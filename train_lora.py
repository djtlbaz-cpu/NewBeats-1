"""
Fine-tune GPT2 with LoRA for lyrics generation using PEFT.
Uses RAG data and synthetic prompt-lyrics pairs.
"""
import os
import json
import random
from pathlib import Path

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset


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
        prompt = f"""Genre: {genre}
Style: {genre_styles[genre]}
Theme: {theme}

{lyrics}"""

        pairs.append({
            "prompt": prompt,
            "lyrics": lyrics,
            "genre": genre
        })

    return pairs


def create_dataset(pairs: list[dict], tokenizer, max_length: int = 256) -> Dataset:
    """Create HF Dataset from training pairs."""

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
    num_epochs: int = 3,
    batch_size: int = 4,
    learning_rate: float = 3e-4,
    max_length: int = 256,
    num_training_pairs: int = 100,
):
    """Fine-tune GPT2 with LoRA."""

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
    dataset = dataset.train_test_split(test_size=0.1)
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
        target_modules=["c_attn", "c_proj", "c_fc", "c_proj"],
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
        learning_rate=learning_rate,
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=1,
        eval_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        warmup_steps=20,
        report_to="none",
        fp16=False,  # Set True if GPU available
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
    }
    with open(os.path.join(output_path, "training_config.json"), "w") as f:
        json.dump(config, f, indent=2)

    print("[+] Training complete!")
    print(f"    Adapter saved to: {output_path}")

    return output_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fine-tune GPT2 with LoRA")
    parser.add_argument("--output", default="lora_adapters", help="Output dir")
    parser.add_argument("--epochs", type=int, default=3, help="Num epochs")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size")
    parser.add_argument("--lr", type=float, default=3e-4, help="Learning rate")
    parser.add_argument("--max-length", type=int, default=256, help="Max tokens")
    parser.add_argument("--num-pairs", type=int, default=100, help="Training pairs")

    args = parser.parse_args()

    train_lora(
        output_dir=args.output,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        max_length=args.max_length,
        num_training_pairs=args.num_pairs,
    )