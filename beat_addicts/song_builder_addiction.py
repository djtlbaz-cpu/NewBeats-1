"""
Enhanced Song Builder using Addiction Formula principles

Generates music with scientifically-proven gratification/anticipation dynamics
"""

import os
import time
import json
from typing import Optional, Callable, Dict, Any

from beat_addicts.lyrics_generator import LyricsGenerator
from beat_addicts.melody_generator import MelodyGenerator
from beat_addicts.addiction_formula import (
    EnergyCurve,
    CompositionGuide,
    SongSection,
    GratificationScorer
)


class AddictionFormulaSongBuilder:
    """Song builder that applies Addiction Formula principles"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.lyrics_gen = LyricsGenerator()
        self.melody_gen: Any = MelodyGenerator()
    
    def build_song_with_addiction_formula(
        self,
        prompt: str,
        genre: str = "pop",
        duration: int = 15,
        progress_callback: Optional[Callable[[float], None]] = None,
        enable_composition_scoring: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a song using Addiction Formula principles
        
        Args:
            prompt: Base creative prompt
            genre: Genre for composition guide
            duration: Song duration in seconds
            progress_callback: Optional callback for progress tracking
            enable_composition_scoring: Score composition against principles
        
        Returns:
            Dict with song paths and composition analysis
        """
        song_id = f"song_{int(time.time())}"
        song_dir = os.path.join(self.output_dir, song_id)
        os.makedirs(song_dir, exist_ok=True)
        
        # Step 1: Generate energy curve
        if progress_callback:
            progress_callback(5)
        energy_curve = EnergyCurve(num_peaks=3)
        
        # Step 2: Create composition guide
        if progress_callback:
            progress_callback(10)
        composition_guide = CompositionGuide(genre=genre, energy_curve=energy_curve)
        
        # Step 3: Generate enhanced lyrics using section guidance
        if progress_callback:
            progress_callback(15)
        lyrics = self._generate_lyrics_with_structure(
            prompt,
            composition_guide,
            progress_callback
        )
        
        # Step 4: Score composition
        if enable_composition_scoring:
            composition_score, score_details = GratificationScorer.score_composition(
                energy_curve
            )
        else:
            composition_score, score_details = None, None
        
        # Save outputs
        if progress_callback:
            progress_callback(85)
        
        lyrics_path = os.path.join(song_dir, f"{song_id}_lyrics.txt")
        with open(lyrics_path, "w", encoding='utf-8') as f:
            f.write(lyrics)
        
        # Save composition analysis
        analysis_path = os.path.join(song_dir, f"{song_id}_composition.json")
        analysis: Dict[str, Any] = {
            "genre": genre,
            "energy_curve": [p.total_energy for p in energy_curve.points],
            "composition_score": composition_score,
            "score_details": score_details,
            "prompt": prompt,
            "lyrics": lyrics
        }
        with open(analysis_path, "w", encoding='utf-8') as f:
            json.dump(analysis, f, indent=2)
        
        # Generate final music (using enhanced prompt with AF guidance)
        if progress_callback:
            progress_callback(90)
        music_prompt = self._build_enhanced_music_prompt(
            prompt,
            genre,
            composition_guide
        )
        
        def _music_progress(x: float) -> None:
            if progress_callback:
                progress_callback(90 + int(x * 0.1))

        melody = self.melody_gen.generate(
            music_prompt,
            duration,
            progress_callback=_music_progress if progress_callback else None,
        )
        
        if progress_callback:
            progress_callback(100)
        
        melody_path = os.path.join(song_dir, f"{song_id}.mp3")
        self.melody_gen.save(melody, melody_path[:-4])
        
        return {
            "song_id": song_id,
            "title": lyrics.split("\n")[0][:50] if lyrics else "Untitled Track",
            "lyrics_path": lyrics_path,
            "song_path": melody_path,
            "analysis_path": analysis_path,
            "composition_score": composition_score,
            "genre": genre,
            "duration": duration,
            "energy_curve": [p.total_energy for p in energy_curve.points]
        }
    
    def _generate_lyrics_with_structure(
        self,
        prompt: str,
        _composition_guide: CompositionGuide,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Generate lyrics following composition structure"""
        
        # Create section-aware prompt
        structure_guidance = """
Create lyrics following this song structure:

VERSE 1: Introduce the problem/emotion, create intrigue
- Short, vivid lines
- Leave listener wanting more
- Build toward hook

PRE-CHORUS: Build emotional intensity
- Hint at the chorus message
- Create anticipation

CHORUS: The payoff, the hook
- Memorable, catchy, repeatable
- Answer the verse's question
- The gratification moment

VERSE 2: Develop the story more
- New perspective or deeper emotion
- Moving the narrative forward
- NOT repeating verse 1

BRIDGE: New territory, peak emotion
- Different melody or perspective
- Most intense emotional moment
- Lead back to final chorus

Create lyrics that follow this psychological flow.
"""
        
        full_prompt = f"{structure_guidance}\n\nCore concept: {prompt}"
        
        lyrics = self.lyrics_gen.generate(
            full_prompt,
            progress_callback=progress_callback
        )
        
        return lyrics
    
    def _generate_music_sections(
        self,
        _prompt: str,
        _genre: str,
        composition_guide: CompositionGuide,
        total_duration: int,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> list[dict[str, Any]]:
        """Generate music sections with appropriate energy for each (simplified)"""
        
        sections_info: list[dict[str, Any]] = []
        
        # Map sections to approximate timing
        section_timings = [
            (SongSection.INTRO, 0, 3),
            (SongSection.VERSE_1, 3, 10),
            (SongSection.PRE_CHORUS, 10, 13),
            (SongSection.CHORUS_1, 13, 18),
            (SongSection.VERSE_2, 18, 25),
            (SongSection.PRE_CHORUS_2, 25, 28),
            (SongSection.CHORUS_2, 28, 33),
            (SongSection.PRIMARY_BRIDGE, 33, 42),
            (SongSection.CHORUS_3, 42, 48),
            (SongSection.OUTRO, 48, total_duration),
        ]
        
        for idx, (section, start_time, end_time) in enumerate(section_timings):
            if end_time > total_duration:
                end_time = total_duration
            
            if start_time >= total_duration:
                break
            
            # Get section guidance from composition guide
            section_config = next(
                (s for s in composition_guide.sections if s.section == section),
                None
            )
            
            sections_info.append({
                "section": section.value,
                "start_time": start_time,
                "end_time": end_time,
                "duration": end_time - start_time,
                "energy_target": section_config.energy_end.total_energy if section_config else 50,
            })
            
            if progress_callback and idx > 0:
                progress_callback(40 + int((idx / len(section_timings)) * 20))
        
        return sections_info
    
    def _build_enhanced_music_prompt(
        self,
        base_prompt: str,
        genre: str,
        _composition_guide: CompositionGuide
    ) -> str:
        """Build comprehensive music generation prompt"""
        
        # Add genre-specific enhancement
        genre_details = self._get_genre_specifics(genre)
        
        # Build structure-aware prompt
        prompt = f"""
Create a {genre} song with the following creative direction:

BASE CONCEPT: {base_prompt}

SONG STRUCTURE (apply Addiction Formula principles):
- Intro: Establish mood and primary sound (0-3 sec)
- Verse 1: Build anticipation, introduce primary elements (3-10 sec)
- Pre-Chorus: Maximum tension buildup (10-13 sec)
- Chorus 1: First gratification moment, memorable hook (13-18 sec)
- Verse 2: Develop further, increase energy vs Verse 1 (18-25 sec)
- Pre-Chorus 2: Higher tension than first (25-28 sec)
- Chorus 2: Bigger than Chorus 1, add layers (28-33 sec)
- Bridge: New territory, emotional/sonic climax (33-42 sec)
- Chorus 3: Peak gratification moment, most powerful (42-48 sec)
- Outro: Resolution or sustained momentum (48+ sec)

GENRE SPECIFICS:
{genre_details}

CRITICAL AF PRINCIPLES:
1. Each section should be slightly more energetic than the previous
2. Use transitions: builds, drops, surprises, or smooth flows
3. Verses explore, choruses celebrate
4. Bridge provides contrast and maximum tension
5. Create anticipation and gratification cycles

ENERGY PROGRESSION:
- Quiet/Sparse → Layered/Rich → Climax → Resolution
- Tension building toward peaks
- Surprise elements for listener engagement
"""
        
        return prompt.strip()
    
    def _get_genre_specifics(self, genre: str) -> str:
        """Get genre-specific composition guidance"""
        
        genre_specs = {
            "pop": """
- Catchy hooks with 2-4 bar loops
- 4/4 time, steady kick drum
- Bright synths for choruses
- Build with added vocals/layers
- Final chorus adds reverb/space
""",
            "house": """
- Four-on-the-floor kick throughout
- Synth bass (sub bass in chorus)
- Build energy with hi-hats opening gradually
- Verse: minimal percussion
- Pre-chorus: dramatic bass drop
- Chorus: full bass + pads
- Bridge: 8-16 bars of buildup
""",
            "lofi": """
- Warm, vintage sound (vinyl crackle, tape saturation)
- Swing feel (not straight 4/4)
- Minimal percussion (soft drums, hi-hats)
- Jazzy chords, minor key preferred
- Reverb on all elements
- Gradual layering from intro to chorus
""",
            "drum_and_bass": """
- Breakbeats (170+ BPM), complex fills
- Heavy bass lines, sub-bass emphasis
- Build tension in verses with break variations
- Chorus: full beat with basslines locked in
- Bridge: stripped down or dramatic shift
- Lots of FX transitions between sections
""",
            "bass_house": """
- Four-on-the-floor kick with side-chain compression
- Deep filtered bass synths (sub-bass in chorus)
- Layered hi-hats with gradual opening
- Verse: minimal, sparse arrangement
- Pre-chorus: dramatic bass drop or synth reveal
- Chorus: full bass + layered pads + filtering
- Bridge: tempo shift or new bass pattern
- All electronic/synth instruments
- Wobble bass LFO automation for tension
- Surprise drops and unexpected transitions
""",
            "experimental_bass": """
- Foundation: deep bass house (808s, filtered basses)
- Polyrhythmic percussion breaks (non-4/4 patterns)
- Granular synth textures with random automation
- Verse: sparse, mysterious, off-beat elements
- Pre-chorus: increasing complexity through layers
- Chorus: layered confusion - resolve with clarity
- Bridge: tempo shifts, filter sweeps, vocal glitches
- Implied tension through production processing
- Semi-resolved ending (ambiguous/unfinished)
- Production-forward storytelling over traditional structure
- Vocal glitches as rhythmic puzzles (not melody)
""",
            "ambient": """
- Pad-based, atmospheric textures
- Minimal percussion (optional)
- Focus on frequency movement over rhythm
- Long releases on sounds
- Reverb as primary effect
- Very gradual energy progression
""",
            "default": """
- Clear section distinction
- Verse: sparse, intimate
- Chorus: full, celebratory
- Bridge: unique texture or effect
- Outro: reflective
"""
        }
        
        return genre_specs.get(genre.lower(), genre_specs["default"])


# Maintain backward compatibility with original SongBuilder
class SongBuilder(AddictionFormulaSongBuilder):
    """Original SongBuilder with Addiction Formula enhancement"""
    
    def build_song(
        self,
        prompt: str,
        duration: int = 15,
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> Dict[str, Any]:
        """Original interface - now uses Addiction Formula by default"""
        result = self.build_song_with_addiction_formula(
            prompt=prompt,
            genre="pop",
            duration=duration,
            progress_callback=progress_callback,
            enable_composition_scoring=True
        )
        
        # Return in original format
        return {
            "title": result["title"],
            "lyrics_path": result["lyrics_path"],
            "song_path": result["song_path"],
            "cover_path": os.path.join(os.path.dirname(result["song_path"]), f"{result['song_id']}_cover.png")
        }
    
    def _build_music_prompt(self, prompt: str) -> str:
        """Original method - return simple prompt"""
        return f"{prompt}. Create a high-energy, well-structured song with clear build-up and memorable hooks."
