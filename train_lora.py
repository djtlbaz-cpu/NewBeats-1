"""
Fine-tune GPT2 with LoRA for lyrics generation using PEFT.
Uses RAG data and synthetic prompt-lyrics pairs.
"""
import os
import json
import random
from pathlib import Path
from typing import Optional, Any

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
try:
    from datasets import Dataset
    DATASETS_AVAILABLE = True
except ImportError:
    Dataset = Any  # type: ignore[assignment]
    DATASETS_AVAILABLE = False


def set_seed(seed: int) -> None:
    """Set random seeds for reproducible training runs."""
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def detect_profile(profile: str = "auto") -> str:
    """Resolve runtime profile to cpu/gpu."""
    profile = (profile or "auto").lower()
    if profile in {"cpu", "gpu"}:
        return profile
    return "gpu" if torch.cuda.is_available() else "cpu"


def get_profile_defaults(profile: str) -> dict[str, Any]:
    """Get tuned defaults for the selected hardware profile."""
    if profile == "gpu":
        return {
            "num_epochs": 4,
            "batch_size": 8,
            "learning_rate": 2e-4,
            "max_length": 256,
            "num_training_pairs": 200,
            "gradient_accumulation_steps": 1,
            "warmup_ratio": 0.03,
            "weight_decay": 0.01,
            "fp16": True,
        }

    return {
        "num_epochs": 2,
        "batch_size": 2,
        "learning_rate": 3e-4,
        "max_length": 192,
        "num_training_pairs": 80,
        "gradient_accumulation_steps": 4,
        "warmup_ratio": 0.05,
        "weight_decay": 0.01,
        "fp16": False,
    }


def load_rag_data(rag_dir: str = "rag_data") -> list[dict]:
    """Load all RAG text files as context data."""
    data = []
    rag_path = Path(rag_dir)
    if not rag_path.exists():
        return []

    for txt_file in rag_path.glob("*.txt"):
        content = txt_file.read_text(encoding="utf-8")
        data.append({
            "filename": txt_file.name,
            "content": content
        })
    return data


def generate_training_pairs(rag_data: list[dict], num_pairs: int = 100) -> list[dict]:
    """Generate synthetic prompt-lyrics training pairs from RAG data."""

    # Genre styles from RAG
    genre_styles = {
        "lo-fi hip hop": "mellow drums, vinyl crackle, relaxed flow, introspective lines",
        "dnb": "energetic rhythm, vivid imagery, confident cadence, punchy couplets",
        "house": "steady four-on-the-floor, catchy hooks, uplifting mood",
        "ambient": "sparse words, long pauses, poetic texture, soft resolutions"
    }

    # Theme templates
    theme_templates = [
        "late night thoughts and city lights",
        "warm nostalgia and bittersweet memories",
        "calm focus for study sessions",
        "gentle storytelling in short verses",
        "hopeful endings under soft synth pads"
    ]

    # Hook examples
    hook_examples = [
        "stay close in the neon glow",
        "we'll study through the silent hours",
        "heartbeats in the bassline",
        "dancing in the rain tonight",
        "chasing dreams through the city"
    ]

    # Verse templates
    verse_templates = [
        "{theme}, {setting}",
        "in the {place}, we {action}",
        "feeling {emotion}, {action}",
        "late night {activity}, {feeling}"
    ]

    settings = ["city lights", "late night studio", "downtown", "your room", "coffee shop"]
    places = ["city", "studio", "room", "streets", "club"]
    actions = ["create", "dream", "flow", "vibe", "groove"]
    emotions = ["chill", "focused", "relaxed", "hyped", "peaceful"]
    activities = ["coding", "studying", "writing", "creating", "chilling"]
    feelings = ["good vibes", "the rhythm", "the beat", "the flow", "the groove"]

    rag_snippets: list[str] = []
    for entry in rag_data:
        content = (entry.get("content") or "").strip()
        if content:
            lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
            rag_snippets.extend(lines[:10])

    pairs = []

    for _ in range(num_pairs):
        genre = random.choice(list(genre_styles.keys()))
        theme = random.choice(theme_templates)
        hook = random.choice(hook_examples)

        # Generate varied verses
        verses = []
        for _ in range(3):
            template = random.choice(verse_templates)
            verse = template.format(
                theme=theme,
                setting=random.choice(settings),
                place=random.choice(places),
                action=random.choice(actions),
                emotion=random.choice(emotions),
                activity=random.choice(activities),
                feeling=random.choice(feelings)
            )
            verses.append(verse.strip(", ").capitalize())

        verses.append(hook)

        lyrics = "\n".join(verses)

        # Build prompt with genre context
        style_hint = random.choice(rag_snippets) if rag_snippets else ""
        prompt = f"""Genre: {genre}
Style: {genre_styles[genre]}
Theme: {theme}
    Style Hint: {style_hint}

{lyrics}"""

        pairs.append({
            "prompt": prompt,
            "lyrics": lyrics,
            "genre": genre
        })

    return pairs


def create_dataset(pairs: list[dict], tokenizer, max_length: int = 256) -> Dataset:
    """Create HF Dataset from training pairs."""
    if not DATASETS_AVAILABLE:
        raise ImportError("datasets is required for training: pip install datasets")

    def tokenize(examples):
        # Concatenate prompt and lyrics, then tokenize
        texts = [p + "\n" + l for p, l in zip(examples["prompt"], examples["lyrics"])]

        # Tokenize with padding and truncation
        tokenized = tokenizer(
            texts,
            truncation=True,
            max_length=max_length,
            padding="max_length",
            return_special_tokens_mask=True,
        )

        # Labels same as input_ids (for causal LM)
        tokenized["labels"] = tokenized["input_ids"].copy()

        return tokenized

    # Convert to HF Dataset
    ds = Dataset.from_list(pairs)

    # Select only needed fields
    ds = ds.select_columns(["prompt", "lyrics"])

    # Tokenize
    ds = ds.map(
        tokenize,
        batched=True,
        remove_columns=ds.column_names,
        desc="Tokenizing"
    )

    return ds


def train_lora(
    output_dir: str = "lora_adapters",
    num_epochs: Optional[int] = None,
    batch_size: Optional[int] = None,
    learning_rate: Optional[float] = None,
    max_length: Optional[int] = None,
    num_training_pairs: Optional[int] = None,
    seed: int = 42,
    gradient_accumulation_steps: Optional[int] = None,
    warmup_ratio: Optional[float] = None,
    weight_decay: Optional[float] = None,
    fp16: Optional[bool] = None,
    profile: str = "auto",
):
    """Fine-tune GPT2 with LoRA."""

    resolved_profile = detect_profile(profile)
    defaults = get_profile_defaults(resolved_profile)

    num_epochs = defaults["num_epochs"] if num_epochs is None else num_epochs
    batch_size = defaults["batch_size"] if batch_size is None else batch_size
    learning_rate = defaults["learning_rate"] if learning_rate is None else learning_rate
    max_length = defaults["max_length"] if max_length is None else max_length
    num_training_pairs = defaults["num_training_pairs"] if num_training_pairs is None else num_training_pairs
    gradient_accumulation_steps = (
        defaults["gradient_accumulation_steps"]
        if gradient_accumulation_steps is None
        else gradient_accumulation_steps
    )
    warmup_ratio = defaults["warmup_ratio"] if warmup_ratio is None else warmup_ratio
    weight_decay = defaults["weight_decay"] if weight_decay is None else weight_decay
    fp16 = defaults["fp16"] if fp16 is None else fp16

    print(f"[*] Training profile: {resolved_profile}")

    set_seed(seed)

    print("[*] Loading base model...")
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token

    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Print base model info
    total_params = sum(p.numel() for p in model.parameters())
    print(f"    Model: {model_name}, {total_params:,} parameters")

    print("[*] Generating training data...")
    rag_data = load_rag_data()
    pairs = generate_training_pairs(rag_data, num_pairs=num_training_pairs)
    print(f"    Generated {len(pairs)} training pairs")

    print("[*] Creating dataset...")
    dataset = create_dataset(pairs, tokenizer, max_length=max_length)

    # Split into train/eval
    eval_size = max(1, int(0.1 * len(dataset)))
    if len(dataset) <= 5:
        eval_size = 1
    dataset = dataset.train_test_split(test_size=eval_size, seed=seed)
    train_ds = dataset["train"]
    eval_ds = dataset["test"]

    print(f"    Train: {len(train_ds)} samples")
    print(f"    Eval: {len(eval_ds)} samples")

    # Configure LoRA
    print("[*] Configuring LoRA...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,          # Rank
        lora_alpha=32, # Alpha scaling
        lora_dropout=0.1,
        target_modules=["c_attn", "c_proj", "c_fc"],
        bias="none",
        inference_mode=False,
    )

    # Apply LoRA to model
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # Causal LM, not MLM
    )

    # Training arguments
    output_path = os.path.join(output_dir, "lyrics_lora")
    training_args = TrainingArguments(
        output_dir=output_path,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        learning_rate=learning_rate,
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=1,
        eval_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        warmup_ratio=warmup_ratio,
        weight_decay=weight_decay,
        seed=seed,
        report_to="none",
        fp16=fp16,
    )

    # Create trainer
    print("[*] Starting training...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        data_collator=data_collator,
    )

    # Train
    trainer.train()

    # Save adapter
    print(f"[*] Saving adapter to {output_path}...")
    model.save_pretrained(output_path)

    # Save config
    config = {
        "model_name": model_name,
        "max_length": max_length,
        "num_epochs": num_epochs,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "num_training_pairs": num_training_pairs,
        "seed": seed,
        "profile": resolved_profile,
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "warmup_ratio": warmup_ratio,
        "weight_decay": weight_decay,
        "fp16": fp16,
    }
    with open(os.path.join(output_path, "training_config.json"), "w") as f:
        json.dump(config, f, indent=2)

    print("[+] Training complete!")
    print(f"    Adapter saved to: {output_path}")

    return output_path


if __name__ == "__main__":
    import argparse

    runtime_profile = detect_profile("auto")
    profile_defaults = get_profile_defaults(runtime_profile)

    parser = argparse.ArgumentParser(description="Fine-tune GPT2 with LoRA")
    parser.add_argument("--output", default="lora_adapters", help="Output dir")
    parser.add_argument("--profile", choices=["auto", "cpu", "gpu"], default="auto", help="Hardware profile")
    parser.add_argument("--epochs", type=int, default=None, help=f"Num epochs (default: {profile_defaults['num_epochs']})")
    parser.add_argument("--batch-size", type=int, default=None, help=f"Batch size (default: {profile_defaults['batch_size']})")
    parser.add_argument("--lr", type=float, default=None, help=f"Learning rate (default: {profile_defaults['learning_rate']})")
    parser.add_argument("--max-length", type=int, default=None, help=f"Max tokens (default: {profile_defaults['max_length']})")
    parser.add_argument("--num-pairs", type=int, default=None, help=f"Training pairs (default: {profile_defaults['num_training_pairs']})")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--grad-accum", type=int, default=None, help=f"Gradient accumulation steps (default: {profile_defaults['gradient_accumulation_steps']})")
    parser.add_argument("--warmup-ratio", type=float, default=None, help=f"Warmup ratio (default: {profile_defaults['warmup_ratio']})")
    parser.add_argument("--weight-decay", type=float, default=None, help=f"Weight decay (default: {profile_defaults['weight_decay']})")
    parser.add_argument("--fp16", dest="fp16", action="store_true", help="Force-enable fp16 training")
    parser.add_argument("--no-fp16", dest="fp16", action="store_false", help="Force-disable fp16 training")
    parser.set_defaults(fp16=None)

    args = parser.parse_args()

    train_lora(
        output_dir=args.output,
        profile=args.profile,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        max_length=args.max_length,
        num_training_pairs=args.num_pairs,
        seed=args.seed,
        gradient_accumulation_steps=args.grad_accum,
        warmup_ratio=args.warmup_ratio,
        weight_decay=args.weight_decay,
        fp16=args.fp16,
    )