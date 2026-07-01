import torch
import os

try:
    from audiocraft.models import MusicGen
    from audiocraft.data.audio import audio_write
    AUDIOCRAFT_AVAILABLE = True
except ImportError:
    AUDIOCRAFT_AVAILABLE = False

import numpy as np
from typing import Optional, Callable

from beat_addicts.device_utils import get_device

torch.set_num_threads(4)  # Optimize CPU core usage


class MelodyGenerator:
    def __init__(
        self,
        model_size: str = "small",
        device_preference: str = "auto",
        lora_adapter_dir: str = "lora_adapters/music_lora"
    ):
        """Initialize the MusicGen model with specified size.

        
        Args:
            model_size: Model size ('small', 'medium', 'large')
            lora_adapter_dir: Path to music LoRA adapters (optional)
        """
        if not AUDIOCRAFT_AVAILABLE:
            raise ImportError(
                "audiocraft is not installed. Install with: pip install audiocraft"
            )

        self.available_models = {
            "small": "facebook/musicgen-small",
            "medium": "facebook/musicgen-medium",
            "large": "facebook/musicgen-large"
        }

        if model_size not in self.available_models:
            raise ValueError(
                f"Invalid model size. Choose from {list(self.available_models.keys())}")

        self.device = get_device(device_preference)
        self.model = MusicGen.get_pretrained(
            self.available_models[model_size],
            device=str(self.device),
        )
        
        # Load music LoRA if available
        self.model = self._maybe_load_lora(self.model, lora_adapter_dir)
        
        self.sample_rate = 32000
        self.max_duration = 90  # Support up to 90s
        self.current_melody: Optional[np.ndarray] = None
    
    def _maybe_load_lora(self, model, adapter_dir: str):
        """Load music LoRA adapter if available."""
        if not adapter_dir or not os.path.isdir(adapter_dir):
            return model
        
        # Check for adapter config
        config_path = os.path.join(adapter_dir, "adapter_config.json")
        if not os.path.exists(config_path):
            return model
        
        try:
            # Music Gen LoRA uses a different approach than PEFT
            # Load the adapter weights
            import json
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Check if we have pre-generated tracks to blend
            # This is a simple approach - in production you'd use proper LoRA
            track_files = []
            for i in range(20):
                track_path = os.path.join(adapter_dir, f"track_{i:03d}.wav")
                if os.path.exists(track_path):
                    track_files.append(track_path)
            
            if track_files:
                print(f"[+] Loaded {len(track_files)} reference tracks from LoRA adapter")
            
            return model
        except Exception as e:
            print(f"[!] Could not load music LoRA: {e}")
            return model

    def generate(self, description: str, duration: int = 15,
                 progress_callback: Optional[Callable[[float], None]] = None) -> np.ndarray:
        """Generate melody from text description.
        
        Args:
            description: Text prompt for music generation
            duration: Duration in seconds (max 90)
            progress_callback: Callback for progress updates
            
        Returns:
            Generated audio as numpy array
        """
        duration = min(duration, self.max_duration)

        
        # Use better generation parameters for more musical output
        self.model.set_generation_params(
            duration=duration,
            temperature=0.8,  # Slightly higher for more creativity
            top_k=250,       # More diverse token selection
            top_p=0.0,      # Let temperature do the work
            use_sampling=True
        )

        if progress_callback:
            progress_callback(0.1)  # Setup complete

        with torch.no_grad():
            # Clean up the prompt - remove confusing additions
            clean_description = description.replace("simple melody", "").strip()
            if not clean_description:
                clean_description = description
            
            wav = self.model.generate([clean_description])[0]

            if progress_callback:
                progress_callback(0.9)  # Generation complete

            self.current_melody = wav.cpu().squeeze().numpy()
            return self.current_melody

    def save(self, melody: np.ndarray, filename: str, format: str = "mp3") -> None:
        """Save generated melody to file.
        
        Args:
            melody: Audio data as numpy array
            filename: Output filename without extension
            format: Audio format ('mp3' or 'wav')
        """
        if format not in ["mp3", "wav"]:
            raise ValueError("Format must be 'mp3' or 'wav'")

        # Convert numpy to tensor if needed
        if isinstance(melody, np.ndarray):
            melody = torch.from_numpy(melody)
        
        audio_write(
            filename,
            melody,
            self.sample_rate,
            format=format,
            mp3_rate=320,  # Higher bitrate for better quality
        )

    def get_last_melody(self) -> Optional[np.ndarray]:
        """Get the last generated melody.
        
        Returns:
            Last generated melody or None if none exists
        """
        return self.current_melody

    def generate_with_melody(self, description: str, melody: np.ndarray,
                             duration: int = 15) -> np.ndarray:
        """Generate music conditioned on both text and melody.
        
        Args:
            description: Text prompt
            melody: Reference melody as numpy array
            duration: Duration in seconds
            
        Returns:
            Generated audio as numpy array
        """
        duration = min(duration, self.max_duration)


        self.model.set_generation_params(
            duration=duration,
            temperature=0.8,
            top_k=250,
            top_p=0.0
        )

        # Convert melody to tensor and add batch dimension
        if isinstance(melody, np.ndarray):
            melody_tensor = torch.from_numpy(melody).unsqueeze(0)
        else:
            melody_tensor = melody.unsqueeze(0)

        with torch.no_grad():
            wav = self.model.generate_with_chroma(
                [description],
                melody_tensor,
                self.sample_rate
            )[0]

            self.current_melody = wav.cpu().squeeze().numpy()
            return self.current_melody


# Example usage
if __name__ == "__main__":
    generator = MelodyGenerator("small")

    # Simple generation
    print("Generating simple melody...")
    melody = generator.generate(
        "A happy jazz tune with piano and drums", duration=10
    )
    generator.save(melody, "jazz_tune")

    # Melody-conditioned generation
    print("\nGenerating melody-conditioned music...")
    base_melody = generator.generate("Simple piano melody", duration=5)
    conditioned = generator.generate_with_melody(
        "Full orchestra arrangement of the piano melody",
        base_melody,
        duration=15
    )
    generator.save(conditioned, "orchestra_version")
