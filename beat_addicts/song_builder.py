import os
import time
from typing import Callable, Optional, Dict, Any, cast

from beat_addicts.lyrics_generator import LyricsGenerator
from beat_addicts.melody_generator import MelodyGenerator


class SongBuilder:
    def __init__(self, output_dir: str = "output") -> None:
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.lyrics_gen = LyricsGenerator()
        self.melody_gen = MelodyGenerator()

        # Progress tracking
        self._progress = 0
        self._progress_steps = 100

    def _update_progress(self, step: int) -> int:
        """Internal progress handler"""
        self._progress = min(self._progress + step, self._progress_steps)
        return self._progress

    def build_song(self, prompt: str, duration: int = 15, progress_callback: Optional[Callable[[float], None]] = None) -> Dict[str, Any]:
        """Generate a complete song with progress tracking"""
        song_id = f"song_{int(time.time())}"
        song_dir = os.path.join(self.output_dir, song_id)
        os.makedirs(song_dir, exist_ok=True)

        # Generate lyrics with progress support
        # Explicitly request verse+hook structure for better phrasing
        def lyrics_progress(x: float) -> None:
            if progress_callback:
                progress_callback(x * 0.4)

        lyrics = cast(str, cast(Any, self.lyrics_gen).generate(
            f"{prompt}. Write lyrics with: 1 vivid setting line, 2-3 short verse lines, final hook phrase.",
            progress_callback=lyrics_progress
        ))
        if progress_callback:
            progress_callback(40)  # Lyrics generation = 40% of work

        # Save lyrics
        lyrics_path = os.path.join(song_dir, f"{song_id}_lyrics.txt")
        with open(lyrics_path, "w", encoding='utf-8') as f:
            f.write(lyrics)
        if progress_callback:
            progress_callback(45)  # File saved

        # Generate melody (60% of progress)
        # Use the actual prompt without confusing additions
        music_prompt = self._build_music_prompt(prompt)
        def melody_progress(x: float) -> None:
            if progress_callback:
                progress_callback(45 + x * 0.55)

        melody = cast(Any, self.melody_gen).generate(
            music_prompt,
            duration,  # Use full duration (up to 90s)
            progress_callback=melody_progress
        )
        if progress_callback:
            progress_callback(100)  # Completion

        # Save melody
        melody_path = os.path.join(song_dir, f"{song_id}.mp3")
        cast(Any, self.melody_gen).save(melody, melody_path[:-4])  # Remove .mp3 extension

        return {
            "title": lyrics.split("\n")[0][:50],  # Trim long titles
            "lyrics_path": lyrics_path,
            "song_path": melody_path,
            "cover_path": os.path.join(song_dir, f"{song_id}_cover.png")
        }
    
    def _build_music_prompt(self, prompt: str) -> str:
        """Build a better prompt for music generation."""
        # Detect genre and enhance prompt
        prompt_lower = prompt.lower()
        
        genre_hints = {
            "bass house": "bass house, energetic beats, synth bass, 4/4 kick drum",
            "drum and bass": "drum and bass, jungle breaks, heavy bass",
            "dnb": "drum and bass, jungle breaks, heavy bass",
            "house": "house music, 4/4 beat, synth pads",
            "lofi": "lo-fi hip hop, chill beats, relaxed vibe",
            "lo-fi": "lo-fi hip hop, chill beats, relaxed vibe",
            "ambient": "ambient, atmospheric, pad sounds",
            "techno": "techno, driving beat, synths"
        }
        
        # Find matching genre hint
        for key, hint in genre_hints.items():
            if key in prompt_lower:
                # Replace genre name with full hint
                enhanced = prompt.replace(key, hint)
                return enhanced
        
        # No specific genre found - just clean up the prompt
        return prompt.replace("lyrics", "").replace("track", "").strip()
