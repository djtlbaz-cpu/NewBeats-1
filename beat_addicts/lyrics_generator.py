import os
import typing as t
import torch
from typing import Any, cast

from transformers import GPT2Tokenizer, GPT2LMHeadModel

from beat_addicts.device_utils import get_device
from beat_addicts.lora_utils import maybe_load_lora_gpt2  # pyright: ignore[reportUnknownVariableType]
from beat_addicts.rag_engine import RagEngine


class LyricsGenerator:
    def __init__(
        self,
        model_name: str = "gpt2",
        device_preference: str = "auto",
        use_rag: bool = True,
        rag_dir: str = "rag_data",
        lora_adapter_dir: str = "lora_adapters/lyrics_lora",
        max_new_tokens: int = 150,
    ):
        self.device = get_device(device_preference)
        self.tokenizer: Any = cast(Any, GPT2Tokenizer.from_pretrained(model_name))  # pyright: ignore[reportUnknownMemberType]

        # GPT2 has no pad_token by default; reuse EOS
        self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model: Any = cast(Any, GPT2LMHeadModel.from_pretrained(model_name).to(self.device))  # pyright: ignore[reportUnknownMemberType, reportArgumentType]
        self.max_new_tokens = max_new_tokens

        self._rag = RagEngine(rag_dir=rag_dir) if use_rag else None

        # Load prompt-to-lyrics guide (best-effort)
        self._lyrics_guide = self._load_lyrics_guide(rag_dir=rag_dir)

        # LoRA is optional/no-op if adapters/peft missing
        self.model = cast(Any, maybe_load_lora_gpt2(self.model, adapter_dir=lora_adapter_dir))

        # Set to eval mode for generation (disables dropout, uses LoRA in inference mode)
        self.model.eval()

    def _load_lyrics_guide(self, rag_dir: str) -> str:
        guide_path = os.path.join(rag_dir, "3_prompt_to_lyrics_guide.txt")
        try:
            with open(guide_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except (FileNotFoundError, UnicodeDecodeError, PermissionError):
            return ""

    def _postprocess_lyrics(self, text: str, max_line_length: int = 50) -> str:
        """
        Enforce a simple, rhythm-friendly layout:
        - 1 vivid setting line (short)
        - 2-3 short verse lines
        - 1 hook-like final line
        """
        if not text:
            return text

        # Normalize
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = "\n".join([ln.strip() for ln in text.split("\n")])
        lines = [ln for ln in text.split("\n") if ln.strip()]

        # Filter out lines that look like they're from the prompt/contract
        filtered: list[str] = []
        for ln in lines:
            ln_clean = ln.strip()
            # Skip lines that are clearly prompt echoes or contractions
            if (
                ln_clean.startswith("-")
                or ln_clean.startswith("*")
                or ln_clean.startswith("1)")
                or ln_clean.startswith("2)")
                or ln_clean.startswith("3)")
                or "output only" in ln_clean.lower()
                or "output contract" in ln_clean.lower()
                or "lyrics:" in ln_clean.lower()
                or "genre:" in ln_clean.lower()
                or "style:" in ln_clean.lower()
            ):
                continue
            # Skip lines that look like they belong to a list (dash + text at start)
            if len(ln_clean) > 0 and ln_clean[0].isdigit() and "." in ln_clean[:3]:
                continue
            filtered.append(ln)

        lines = filtered if filtered else lines

        # Enforce max 6 lines total
        if len(lines) > 6:
            lines = lines[:6]

        # Aggressively shorten overly long lines (split on commas/sentences)
        short_lines: list[str] = []
        for ln in lines:
            ln = ln.strip()
            if len(ln) > max_line_length:
                # Split on common separators to make shorter
                for sep in ["--", "- ", ", "]:
                    if sep in ln:
                        parts = ln.split(sep)
                        for p in parts[:3]:  # Take max 3 parts
                            p = p.strip()
                            if p and len(p) <= max_line_length:
                                short_lines.append(p)
                        break
                else:
                    # No separator found, truncate
                    short_lines.append(ln[:max_line_length])
            else:
                short_lines.append(ln)

        lines = short_lines

        # If we got too few lines, don't over-invent; just return normalized text
        if len(lines) < 3:
            return "\n".join(lines).strip()

        # Attempt to ensure hook-like final line
        hook_keywords = [
            "stay ",
            "heartbeats",
            "neon",
            "silent hours",
            "bassline",
            "hook",
            "we'll",
            "we'll",
            "love",
            "promise",
        ]
        final = lines[-1].lower()
        if not any(k in final for k in hook_keywords):
            # Replace last line with a generic hook phrase matching the guide vibe
            fallback_hooks = [
                "stay close in the neon glow",
                "we'll study through the silent hours",
                "heartbeats in the bassline",
            ]
            # Choose the fallback that best matches the existing line sentiment
            # (cheap heuristic: prefer longer/stronger overlap by words)
            best = fallback_hooks[0]
            best_score = -1
            tokens = set(final.split())
            for h in fallback_hooks:
                score = len(tokens & set(h.lower().split()))
                if score > best_score:
                    best_score = score
                    best = h
            lines[-1] = best

        return "\n".join(lines).strip()

    def _build_prompt(self, prompt: str) -> str:
        prompt = prompt or ""
        genre = "lo-fi hip hop"

        prompt_lower = prompt.lower()
        if any(g in prompt_lower for g in ["dnb", "drum and bass", "jungle"]):
            genre = "drum and bass"
        elif any(g in prompt_lower for g in ["house", "edm"]):
            genre = "house"
        elif any(g in prompt_lower for g in ["ambient", "chill", "relax"]):
            genre = "ambient"

        context_parts: list[str] = []
        if self._rag:
            theme_context = self._rag.build_context(prompt, top_k=1, max_chars=150)
            if theme_context:
                context_parts.append(theme_context)

        prefix = prompt.strip()
        if not prefix:
            prefix = "lofi lyrics"

        # Keep prompt SHORT
        parts = [prefix]
        if context_parts:
            parts.append(context_parts[0][:100])
        parts.append("Genre: " + genre)

        # Brief structure reminder
        parts.append("Format: setting line, 2-3 verses, final hook")

        return "\n".join(parts) + "\n\nLyrics:\n"

    def generate(
        self,
        prompt: str,
        max_new_tokens: t.Optional[int] = None,
        progress_callback: t.Optional[t.Callable[[float], None]] = None,
    ) -> str:
        final_prompt = self._build_prompt(prompt)

        inputs: Any = self.tokenizer(final_prompt, return_tensors="pt").to(self.device)

        if progress_callback:
            progress_callback(0.2)  # Encoding done

        # Use slightly higher temperature for more creative output
        max_tokens = max_new_tokens or self.max_new_tokens

        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_new_tokens=max_tokens,
                temperature=0.8,
                do_sample=True,
                repetition_penalty=1.3,
                top_p=0.92,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        if progress_callback:
            progress_callback(0.8)  # Generation done

        # Decode and extract just lyrics after "Lyrics:"
        # Use rfind to find the LAST "Lyrics:" (after the contract)
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        lyrics_marker = result.rfind("Lyrics:")
        if lyrics_marker != -1:
            result = result[lyrics_marker + len("Lyrics:"):].strip()

        return self._postprocess_lyrics(result)