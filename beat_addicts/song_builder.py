import os
import time
import inspect
import torch
torch.set_default_device('cpu')

from beat_addicts.lyrics_generator import LyricsGenerator
from beat_addicts.melody_generator import MelodyGenerator

class SongBuilder:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.lyrics_gen = LyricsGenerator()
        self.melody_gen = MelodyGenerator()
        
        # Progress tracking
        self._progress = 0
        self._progress_steps = 100

    def _update_progress(self, step):
        """Internal progress handler"""
        self._progress = min(self._progress + step, self._progress_steps)
        return self._progress

    def build_song(self, prompt, duration=15, progress_callback=None):
        """Generate a complete song with progress tracking"""
        song_id = f"song_{int(time.time())}"
        song_dir = os.path.join(self.output_dir, song_id)
        os.makedirs(song_dir, exist_ok=True)

        # Generate lyrics with progress support
        lyrics = self.lyrics_gen.generate(
            f"Song about {prompt}",
            progress_callback=lambda x: progress_callback(x*0.4) if progress_callback else None
        )
        if progress_callback:
            progress_callback(40)  # Lyrics generation = 40% of work

        # Save lyrics
        lyrics_path = os.path.join(song_dir, f"{song_id}_lyrics.txt")
        with open(lyrics_path, "w", encoding='utf-8') as f:
            f.write(lyrics)
        if progress_callback:
            progress_callback(45)  # File saved

        # Generate melody (60% of progress)
        melody = self.melody_gen.generate(
            f"{prompt} simple melody",
            min(duration, 30),  # Duration cap
            progress_callback=lambda x: progress_callback(45 + x*0.55) if progress_callback else None
        )
        if progress_callback:
            progress_callback(100)  # Completion

        # Save melody
        melody_path = os.path.join(song_dir, f"{song_id}.mp3")
        self.melody_gen.save(melody, melody_path[:-4])  # Remove .mp3 extension

        return {
            "title": lyrics.split("\n")[0][:50],  # Trim long titles
            "lyrics_path": lyrics_path,
            "song_path": melody_path,
            "cover_path": os.path.join(song_dir, f"{song_id}_cover.png")
        }