import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import numpy as np
from typing import Optional, Callable

torch.set_default_device('cpu')
torch.set_num_threads(4)  # Optimize CPU core usage


class MelodyGenerator:
    def __init__(self, model_size: str = "small"):
        """Initialize the MusicGen model with specified size.

        Args:
            model_size: Model size ('small', 'medium', 'large')
        """
        self.available_models = {
            "small": "facebook/musicgen-small",
            "medium": "facebook/musicgen-medium",
            "large": "facebook/musicgen-large"
        }

        if model_size not in self.available_models:
            raise ValueError(
                f"Invalid model size. Choose from {list(self.available_models.keys())}")

        self.model = MusicGen.get_pretrained(
            self.available_models[model_size],
            device='cpu'
        )
        self.model.set_default_device('cpu')
        self.sample_rate = 32000
        self.max_duration = 30  # Safety cap for CPU
        self.current_melody: Optional[np.ndarray] = None

    def generate(self, description: str, duration: int = 15,
                 progress_callback: Optional[Callable[[float], None]] = None) -> np.ndarray:
        """Generate melody from text description.

        Args:
            description: Text prompt for music generation
            duration: Duration in seconds (max 30)
            progress_callback: Callback for progress updates

        Returns:
            Generated audio as numpy array
        """
        duration = min(duration, self.max_duration)

        self.model.set_generation_params(
            duration=duration,
            temperature=0.7,
            top_k=100,
            top_p=0.8,
            use_sampling=True
        )

        if progress_callback:
            progress_callback(0.1)  # Setup complete

        with torch.no_grad():
            wav = self.model.generate([description])[0]

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

        audio_write(
            filename,
            torch.from_numpy(melody),
            self.sample_rate,
            format=format,
            loudness_compression=True
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
            temperature=0.7,
            top_k=100,
            top_p=0.8
        )

        # Convert melody to tensor and add batch dimension
        melody_tensor = torch.from_numpy(melody).unsqueeze(0)

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
        "A happy jazz tune with piano and drums", duration=10)
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
