from __future__ import annotations

import os
from typing import Optional


def maybe_load_lora_gpt2(
    model,
    adapter_dir: str = "lora_adapters",
):
    """
    Bulletproof LoRA loader for GPT-2-style models using PEFT.

    - If adapter_dir doesn't exist or PEFT isn't installed -> no-op (returns model)
    - If adapter weights/config are missing -> no-op
    - Never raises (best-effort).
    """
    try:
        if not adapter_dir or not os.path.isdir(adapter_dir):
            return model

        # Basic presence check
        # PEFT typically uses adapter_model.bin / adapter_model.safetensors + adapter_config.json
        required_markers = [
            os.path.join(adapter_dir, "adapter_config.json"),
        ]
        if not all(os.path.exists(p) for p in required_markers):
            return model

        from peft import PeftModel  # type: ignore

        # from_pretrained will load whatever adapter weights are present
        model = PeftModel.from_pretrained(model, adapter_dir)
        return model
    except Exception:
        return model
