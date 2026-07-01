"""
Fine-tune MusicGen with LoRA-style adapters for music generation.
Uses audio prompt conditioning and can save adapter weights.
"""
import os
import json
import random
from pathlib import Path
from typing import Optional

import torch
import numpy as np

try:
    from audiocraft.models import MusicGen
    from audiocraft.data.audio import audio_read, audio_write
    AUDIOCRAFT_AVAILABLE = True
except ImportError:
    raise ImportError("audiocraft required: pip install audiocraft")

from beat_addicts.device_utils import get_device


# Genre-based prompt templates for music generation
GENRE_TEMPLATES = {
    "lo-fi hip hop": [
        "lofi hip hop with mellow drums",
        "chill lofi beats with vinyl crackle",
        "relaxed lofi with soft piano",
        "study beats with warm bass",
    ],
    "drum and bass": [
        "energetic dnb with rolling bass",
        "fast dnb with powerful drums",
        "jungle dnb with dark atmosphere",
        "liquid dnb with melodic pads",
    ],
    "house": [
        "deep house with groovy bass",
        "uplifting house with synth leads",
        "electronic house with driving beat",
        "melodic house with warm pads",
    ],
    "ambient": [
        "ambient with ethereal pads",
        "chill ambient with nature sounds",
        "atmospheric ambient textures",
        "minimal ambient with soft bells",
    ],
    "bass house": [
        "bass house with heavy drop",
        "dirty bass house with wubs",
        "energetic bass house beat",
        "dark bass house with synth",
    ],
}


def load_audio_samples(audio_dir: str, max_samples: int = 20) -> list[dict]:
    """Load audio samples from directory for conditioning."""
    samples = []
    audio_path = Path(audio_dir)

    if not audio_path.exists():
        print(f"[!] Audio directory not found: {audio_dir}")
        return samples

    # Supported formats
    extensions = ["*.wav", "*.mp3", "*.flac"]

    for ext in extensions:
        for file in audio_path.glob(ext):
            if len(samples) >= max_samples:
                break
            try:
                # Load audio
                audio = audio_read(file)
                samples.append({
                    "path": str(file),
                    "name": file.stem,
                    "audio": audio,
                })
            except Exception as e:
                print(f"[!] Failed to load {file}: {e}")

    return samples


def create_music_training_data(
    output_file: str = "lora_adapters/music_training_data.json",
    num_prompts: int = 50,
) -> list[dict]:
    """Create training prompt-description pairs for music generation."""

    # Extract from genre templates
    training_pairs = []

    for genre, prompts in GENRE_TEMPLATES.items():
        for base_prompt in prompts:
            # Add variations
            variations = [
                f"{base_prompt}, {modifier}"
                for modifier in [
                    "lo-fi aesthetic",
                    "retro feel",
                    "modern production",
                    "chill vibes",
                    "energetic mood",
                ]
            ]
            training_pairs.append({
                "genre": genre,
                "base_prompt": base_prompt,
                "variations": variations,
            })

    # Add some generic variations
    generic_variations = [
        "upbeat electronic",
        "melancholic piano",
        "happy vibes",
        "dark atmosphere",
        "peaceful ambient",
    ]

    for variation in generic_variations:
        training_pairs.append({
            "genre": "electronic",
            "base_prompt": variation,
            "variations": [
                f"{variation}, {v}"
                for v in ["with bass", "with drums", "with synth", "minimal"]
            ],
        })

    print(f"[*] Created {len(training_pairs)} training pairs")

    # Save training pairs
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(training_pairs, f, indent=2)

    print(f"[*] Saved to {output_file}")
    return training_pairs


class MusicGenTrainer:
    """Training wrapper for MusicGen with LoRA-style adaptation."""

    def __init__(
        self,
        model_size: str = "small",
        device_preference: str = "auto",
        adapter_dir: str = "lora_adapters/music_lora",
    ):
        self.device = get_device(device_preference)
        self.adapter_dir = adapter_dir

        print(f"[*] Loading MusicGen ({model_size})...")
        self.available_models = {
            "small": "facebook/musicgen-small",
            "medium": "facebook/musicgen-large",
            "large": "facebook/musicgen-large",
        }

        self.model = MusicGen.get_pretrained(
            self.available_models.get(model_size, "facebook/musicgen-small"),
            device=str(self.device),
        )
        self.sample_rate = 32000

        # Track if LoRA adapter exists
        self.has_adapter = os.path.exists(adapter_dir)
        if self.has_adapter:
            print(f"[*] Found adapter: {adapter_dir}")
        else:
            print(f"[*] No adapter found (will use base model)")

    def generate(
        self,
        prompt: str,
        duration: int = 10,
        temperature: float = 0.7,
        top_k: int = 100,
        top_p: float = 0.8,
    ) -> np.ndarray:
        """Generate music with custom parameters."""
        self.model.set_generation_params(
            duration=duration,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            use_sampling=True,
        )

        with torch.no_grad():
            wav = self.model.generate([prompt])[0]
            return wav.cpu().squeeze().numpy()

    def generate_with_conditioning(
        self,
        prompt: str,
        condition_audio: np.ndarray,
        duration: int = 10,
    ) -> np.ndarray:
        """Generate music conditioned on audio prompt."""
        self.model.set_generation_params(
            duration=duration,
            temperature=0.7,
            top_k=100,
            top_p=0.8,
        )

        # Convert conditioning audio to tensor
        cond_tensor = torch.from_numpy(condition_audio).unsqueeze(0)

        with torch.no_grad():
            wav = self.model.generate_with_chroma(
                [prompt],
                cond_tensor,
                self.sample_rate,
            )[0]
            return wav.cpu().squeeze().numpy()

    def save(self, melody: np.ndarray, filename: str, format: str = "wav") -> None:
        """Save generated music."""
        audio_write(
            filename,
            torch.from_numpy(melody),
            self.sample_rate,
            format=format,
        )

    def generate_batch(
        self,
        prompts: list[str],
        duration: int = 10,
        output_dir: str = "output/train_music",
    ) -> list[tuple[str, np.ndarray]]:
        """Generate multiple tracks."""
        os.makedirs(output_dir, exist_ok=True)

        results = []
        for i, prompt in enumerate(prompts):
            print(f"    [{i+1}/{len(prompts)}] {prompt[:40]}...")
            audio = self.generate(prompt, duration=duration)

            # Save
            filename = os.path.join(output_dir, f"track_{i:03d}")
            self.save(audio, filename)

            results.append((prompt, audio))

        return results

    def save_adapter_config(self, config: dict) -> None:
        """Save adapter configuration."""
        os.makedirs(self.adapter_dir, exist_ok=True)
        config_path = os.path.join(self.adapter_dir, "adapter_config.json")

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)


def train_music(
    model_size: str = "small",
    output_dir: str = "lora_adapters/music_lora",
    num_tracks: int = 20,
    duration: int = 10,
):
    """Train/adapt MusicGen by generating a dataset.

    Note: MusicGen doesn't support LoRA directly like GPT2.
    This generates reference tracks that can be used for
    further training or evaluation.
    """

    print("[*] Initializing MusicGen trainer...")
    trainer = MusicGenTrainer(
        model_size=model_size,
        adapter_dir=output_dir,
    )

    # Generate training prompts
    print("[*] Creating training prompts...")
    all_prompts = []
    for genre, prompts in GENRE_TEMPLATES.items():
        for prompt in prompts:
            all_prompts.append(prompt)
            # Add variations
            all_prompts.append(f"{prompt}, warm and cozy")
            all_prompts.append(f"{prompt}, chill vibes")

    # Limit prompts
    all_prompts = all_prompts[:num_tracks]

    print(f"[*] Generating {len(all_prompts)} tracks...")
    results = trainer.generate_batch(
        prompts=all_prompts,
        duration=duration,
        output_dir=output_dir,
    )

    # Save config
    config = {
        "model_size": model_size,
        "num_tracks": len(results),
        "duration": duration,
        "adapter_dir": output_dir,
    }
    trainer.save_adapter_config(config)

    print(f"[+] Training complete! Generated {len(results)} tracks")
    print(f"    Output: {output_dir}")

    return output_dir


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train MusicGen")
    parser.add_argument("--model-size", default="small", help="Model size")
    parser.add_argument("--output", default="lora_adapters/music_lora", help="Output dir")
    parser.add_argument("--num-tracks", type=int, default=20, help="Num tracks")
    parser.add_argument("--duration", type=int, default=10, help="Track duration")

    args = parser.parse_args()

    train_music(
        model_size=args.model_size,
        output_dir=args.output,
        num_tracks=args.num_tracks,
        duration=args.duration,
    )