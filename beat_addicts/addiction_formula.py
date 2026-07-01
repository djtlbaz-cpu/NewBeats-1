"""
Addiction Formula Implementation for Beat Addicts

Implements songwriting principles from "The Addiction Formula" by Friedemann Findeisen.
Focuses on energy curves, gratification/anticipation dynamics, and song structure.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Tuple, Optional
import numpy as np


class TransitionType(Enum):
    """9 transition types from the Addiction Formula"""
    JUMP = "jump"              # Abrupt hype increase
    SMOOTH = "smooth"          # Gradual hype + tension
    DROP = "drop"              # Abrupt hype decrease
    SURPRISE = "surprise"      # Build tension then drop hype
    OVERSHOOT = "overshoot"    # Build more tension than needed
    FALSE_PROMISE = "false_promise"  # Build tension, same hype
    FLATLINE = "flatline"      # No change in hype
    LIFT = "lift"              # Less tension than needed for hype increase
    NEGATIVE_TENSION = "negative_tension"  # Gradual decrease to lower hype


class BuildUpTechnique(Enum):
    """Three ways to create anticipation leading to energy peaks"""
    HYPE_ONLY = "hype_only"          # Increase hype every 4-8 bars (jumpy, chaotic effect)
    TENSION_ONLY = "tension_only"    # Use only tension (smooth, mysterious, less direction)
    COMBINED = "combined"             # Hype + tension together (most popular, best for energy peaks)


class FrequencySpectrum(Enum):
    """Frequency ranges for texture-based hype setting"""
    NONE = "none"              # Silent/minimal (lowest hype)
    HIGHS_ONLY = "highs"       # Piano right hand, high guitar
    MIDS_ONLY = "mids"         # Piano chords, rhythm guitar
    LOWS_ONLY = "lows"         # Bass, low piano
    MIDS_HIGHS = "mids_highs"  # Mid + high range
    LOWS_MIDS = "lows_mids"    # Low + mid range
    LOWS_HIGHS = "lows_highs"  # Low + high (sparse middle)
    FULL = "full"              # All three ranges (highest hype)


class TensionType(Enum):
    """Types of tension in arrangement"""
    REGULAR = "regular"              # Adding/removing instruments mid-section
    IMPLIED = "implied"              # Noticeably stripping out elements to create missing element pull


class SongElement(Enum):
    """Six elements of songwriting - all work together to create energy"""
    ARRANGEMENT = "arrangement"      # Most powerful - instrument texture and frequency
    HARMONY = "harmony"              # Chord progressions and harmonic movement
    RHYTHM = "rhythm"                # Beat patterns and rhythmic density
    PART_WRITING = "part_writing"    # Individual instrument lines and notes
    LYRICS = "lyrics"                # Lyrical content and vocal delivery
    PRODUCTION = "production"        # Effects, mixing, filters, sound design


class VocalMode(Enum):
    """Four main vocal modes for controlling hype"""
    SPEECH = "speech"                # Rap-like, conversational (low-mid hype)
    NEUTRAL = "neutral"              # Natural singing voice (medium hype)
    FALSETTO = "falsetto"            # Light, airy quality (medium-high hype)
    BELTING = "belting"              # Powerful, projected, edge (highest hype)


class VocalEffect(Enum):
    """Effects that can be applied to vocals for energy shaping"""
    TWANG = "twang"                  # Oral/nasal resonance (raises hype)
    VIBRATO = "vibrato"              # Oscillation on held notes (adds rhythm, raises hype)
    ORNAMENTATIONS = "ornamentations"  # Fast melodic sequences (RnB style, raises hype)
    DISTORTION = "distortion"        # Adds edge/aggression (raises hype in rock/metal)


class VocalDistortionType(Enum):
    """Types of vocal distortion by pitch (lowest to highest hype)"""
    GROWLING = "growling"            # Low pitch distortion (rock/metal)
    SHOUTING = "shouting"            # Mid-range pitch distortion
    SCREAMING = "screaming"          # High pitch distortion (highest hype)
    CURBING = "curbing"              # Very subtle distortion (pop music)


class VocalMelodyTechnique(Enum):
    """Melodic approaches for controlling vocal energy"""
    ASCENDING = "ascending"          # Rise in pitch across section (creates tension)
    DESCENDING = "descending"        # Fall in pitch across section (releases tension)
    ONE_NOTE = "one_note"            # Single repeated note (lowest hype)
    VARIED = "varied"                # Many different notes (highest hype)


class VocalTensionTechnique(Enum):
    """Specific techniques for creating vocal tension"""
    ASCENDING_MELODY = "ascending_melody"      # Gradually raise pitch
    MODE_SHIFT = "mode_shift"                  # Change vocal mode mid-section
    POWER_INCREASE = "power_increase"          # Gradually increase singing intensity
    TENSE_NOTES = "tense_notes"                # Hit 3rd/7th of V chord (classical, risky)
    EFFECT_CRESCENDO = "effect_crescendo"      # Gradually add twang or distortion


class VocalImpliedTensionTechnique(Enum):
    """Techniques for implied tension with vocals"""
    SUBTRACT_MELODY = "subtract_melody"        # Remove vocals entirely
    TENSE_ONE_NOTE = "tense_one_note"         # One-note melody not in tonic triad
    SPACE = "space"                            # Use breathing/rests (fight lyrical chains)
    ATTITUDE_CONTRAST = "attitude_contrast"    # Low-energy vocals over high-energy music or vice versa


class HarmonyTension(Enum):
    """Harmonic starting positions for sections"""
    TONIC = "tonic"                  # I, vi, iii (major); i, VI, III (minor) - NO natural tension
    SUBDOMINANT = "subdominant"      # IV, ii, II (major); iv, IV (minor) - MEDIUM tension
    DOMINANT = "dominant"            # V, bVII (major); V, VII, bII, v (minor) - HIGH tension


class RhythmicSubdivision(Enum):
    """Note subdivisions for controlling rhythm-based hype"""
    WHOLE = "sub1"                   # Whole note - lowest hype
    HALF = "sub2"                    # Half note
    QUARTER = "sub4"                 # Quarter note - medium hype
    EIGHTH = "sub8"                  # Eighth note - higher hype
    SIXTEENTH = "sub16"              # Sixteenth note - highest hype


class RhythmicStyle(Enum):
    """Rhythmic approaches for creating tension"""
    LEGATO = "legato"                # Smooth, connected (higher hype than staccato)
    STACCATO = "staccato"            # Short, separated (lower hype)
    BROKEN_FLOW = "broken_flow"      # Hinted at higher subdivision (implied tension)
    CONTRARY = "contrary_movement"   # Drums off-beat (implied tension)


class VocalRangePosition(Enum):
    """Pitch position within vocal range"""
    LOWEST = "lowest"                # Lowest notes in verse (lowest hype)
    LOWER = "lower"                  # Lower-mid range
    MIDDLE = "middle"                # Center range
    HIGHER = "higher"                # Upper-mid range
    HIGHEST = "highest"              # Highest notes in chorus (highest hype)


class GuitarPlayingMode(Enum):
    """Guitar tone modes - fundamental to hype level"""
    DISTORTED = "distorted"          # Highest hype, aggressive, thick
    CLEAN = "clean"                  # Lower hype, natural, clear


class GuitarPlayingStyle(Enum):
    """Specific guitar techniques for controlling hype (lowest to highest)"""
    SINGLE_NOTES_MINIMAL = "single_notes_minimal"      # Single notes, sparse
    SINGLE_NOTES_STRUCK = "single_notes_struck"        # Individual struck notes
    SINGLE_NOTES_HARMONIC = "single_notes_harmonic"    # Harmonics (bell-like)
    CHORD_ARPEGGIO = "chord_arpeggio"                  # Chord broken into individual notes
    CHORD_PALM_MUTED = "chord_palm_muted"             # Muted chord (muffled)
    CHORD_STRUMMED = "chord_strummed"                 # Full strummed chord (highest hype)


class GuitarPickingStyle(Enum):
    """Guitar picking approach - affects overall hype before first note"""
    FINGERS = "fingers"              # Fingerstyle - softer
    SOFT_PICK = "soft_pick"          # Soft pick - warmer
    MEDIUM_PICK = "medium_pick"      # Standard pick - neutral
    HARD_PICK = "hard_pick"          # Hard pick - brighter, more attack


class GuitarTensionTechnique(Enum):
    """Techniques for creating tension on guitar"""
    PALM_MUTE_CRESCENDO = "palm_mute_crescendo"        # Release palm mute gradually (natural crescendo)
    VIBRATO = "vibrato"                                # Oscillation on held notes
    TREMOLO_BAR_VIBRATO = "tremolo_bar_vibrato"        # Whammy bar oscillation
    TREMOLO_BAR_DROP = "tremolo_bar_drop"              # Pitch drop with whammy bar
    SQUEEZE_HARMONIC = "squeeze_harmonic"              # Pinch harmonic squeal
    SLOW_BEND = "slow_bend"                            # Gradual pitch rise
    PICK_SLIDE = "pick_slide"                          # Scraping pick across strings
    CHUG = "chug"                                      # Muted rhythmic strike


class GuitarImpliedTensionTechnique(Enum):
    """Techniques for implied tension with guitar"""
    CLOSED_PALM_MUTE = "closed_palm_mute"              # Heavily muted (missing clarity)
    SLIDE_REPEATED = "slide_repeated"                  # Multiple slides in section
    DRONE = "drone"                                    # Low open string riff (sinister/hypnotic)


class BassPlayingStyle(Enum):
    """Bass techniques for controlling hype (lowest to highest)"""
    SINGLE_NOTE_PALM_MUTED = "single_note_palm_muted"  # Lowest hype
    SINGLE_NOTE_PLUCKED = "single_note_plucked"        # Single note, clear
    SINGLE_NOTE_PICKED = "single_note_picked"          # Single note, pick attack
    CHORD_PLUCKED = "chord_plucked"                    # Fingerstyle chord
    CHORD_PICKED = "chord_picked"                      # Pick-struck chord
    SLAP = "slap"                                      # Percussive slap (highest hype)


class BassImpliedTensionTechnique(Enum):
    """Techniques for implied tension with bass"""
    SLIDE_REPEATED = "slide_repeated"                  # Multiple slides
    DRONE = "drone"                                    # Continuous low note (friction with chords)


class DrumCymbalChoice(Enum):
    """Cymbal/drum choices for setting hype (lowest to highest)"""
    RIMS_ONLY = "rims_only"                    # Rim click/shot only - lowest hype
    RIDE = "ride"                              # Ride cymbal - warm, complex
    CLOSED_HIHAT = "closed_hihat"              # Closed hi-hat - standard
    OPEN_HIHAT = "open_hihat"                  # Open hi-hat - washy, higher
    TOMS = "toms"                              # Tom drums - punchy
    CRASH = "crash"                            # Crash cymbal - highest hype


class DrumTensionTechnique(Enum):
    """Techniques for creating tension with drums"""
    HIHAT_GRADUAL_OPEN = "hihat_gradual_open"          # Slowly open hi-hat (crescendo effect)
    RIDE_BELL_TO_WASH = "ride_bell_to_wash"            # Move from bell (ping) to wash sound
    FILL_INTRODUCTION = "fill_introduction"            # Tom fills, snare fills, crashes
    SNARE_ROLL = "snare_roll"                          # Extended snare roll
    CYMBAL_ROLL = "cymbal_roll"                        # Extended cymbal roll


class DrumImpliedTensionTechnique(Enum):
    """Techniques for implied tension with drums"""
    HALFOPEN_HIHAT = "halfopen_hihat"                  # Half-open hi-hat groove (familiar incomplete pattern)
    TOM_GROOVE = "tom_groove"                          # Tom rhythm without full beat (feels like fill)
    SNARE_GROOVE = "snare_groove"                      # Snare-focused groove (feels incomplete)
    INCOMPLETE_BEAT = "incomplete_beat"                # Missing kick, snare, or hi-hat (audience expects full beat)


class SynthFilterTechnique(Enum):
    """Synth-specific techniques for tension/hype"""
    LOWPASS_FILTER_OPENING = "lowpass_filter_opening"  # Slowly raise cutoff frequency (tension)
    LOWPASS_FILTER_CLOSING = "lowpass_filter_closing"  # Lower cutoff (reduce hype/energy)


class LyricHypeMethod(Enum):
    """Methods for controlling hype through lyrics"""
    SCOPE_SPECIFIC = "scope_specific"                   # Detailed, specific language (low hype)
    SCOPE_GENERAL = "scope_general"                     # Big picture, meta language (high hype)
    POWER_WORDS = "power_words"                         # Emotionally charged or meaningful words


class LyricTensionTechnique(Enum):
    """Techniques for creating tension through lyrical content"""
    STORY_PROGRESSION = "story_progression"             # Continuous narrative across sections
    CLIFFHANGER = "cliffhanger"                         # Question, surprise, or cut-off (contentual)
    PICKUP = "pickup"                                   # Vocal line enters before section starts
    SPLIT_LINE = "split_line"                           # Line split across section boundary
    OUROBOROS_MELODY = "ouroboros_melody"               # Lyrical blocks misaligned with music


class LyricImpliedTensionTechnique(Enum):
    """Techniques for implied tension through lyrics"""
    CONTRAST_LOW_ENERGY_LYRICS = "contrast_low_energy"  # Low-energy lyrics to high-energy music
    CONTRAST_HIGH_ENERGY_LYRICS = "contrast_high_energy" # High-energy lyrics to low-energy music
    ASYMMETRIC_PHRASING = "asymmetric_phrasing"         # 3 or 5 line blocks instead of 4
    INTERNAL_SPLIT_LINES = "internal_split_lines"       # Pauses within a section (not across boundary)


class LyricSectionRole(Enum):
    """Specific lyrical role for each song section"""
    INTRO = "intro"                          # Establish mood, introduce vocals early
    FIRST_VERSE = "first_verse"              # Introduce characters, specific details, grab attention
    PRE_CHORUS = "pre_chorus"                # Lead into chorus, introduce inciting incident
    CHORUS = "chorus"                        # Multi-faceted, big-picture, multiple interpretations
    SECOND_VERSE = "second_verse"            # Deepen story, zoom out, higher energy than verse 1
    BRIDGE = "bridge"                        # Surprise element, style change, story turn
    FINAL_CHORUS = "final_chorus"            # Drive point home, reinforce main message
    OUTRO = "outro"                          # Return to intro mood or end on high energy


class ProductionHypeMethod(Enum):
    """Production methods for setting hype"""
    FATTENING = "fattening"                  # Layering, compression, filters (makes thick)
    THINNING = "thinning"                    # Removing layers, opening filters (makes thin)
    PERCEIVED_VOLUME = "perceived_volume"    # Compression, volume automation
    DIMENSION_SPACE = "dimension_space"      # Reverb, delay, stereo widening
    NEW_INSTRUMENTS = "new_instruments"      # Adding pads, percussion, synths, samples
    PROCESSING = "processing"                # Any effect applied noticeably


class ProductionTensionMethod(Enum):
    """Production methods for creating tension"""
    AUTOMATION_FATTENING = "automation_fattening"            # Gradually fade in layers
    AUTOMATION_FILTER = "automation_filter"                  # Gradually change cutoff frequency
    AUTOMATION_VOLUME = "automation_volume"                  # Gradual volume crescendo
    AUTOMATION_SPACE = "automation_space"                    # Gradually add reverb/delay
    AUTOMATION_EFFECTS = "automation_effects"                # Gradually add/modify processing
    SOUND_EFFECT_UPLIFTER = "sound_effect_uplifter"         # Rising noise sweep
    SOUND_EFFECT_DOWNLIFTER = "sound_effect_downlifter"     # Falling noise sweep
    SOUND_EFFECT_WHOOSH = "sound_effect_whoosh"             # Sweeping transition sound
    SOUND_EFFECT_REVERSE = "sound_effect_reverse"           # Reversed audio effect


class ProductionImpliedTensionMethod(Enum):
    """Production methods for implied tension"""
    HIGHPASS_FILTER = "highpass_filter"                      # Cut low frequencies (thin out)
    LOWPASS_FILTER = "lowpass_filter"                        # Cut high frequencies (dull)
    AUTO_FILTER = "auto_filter"                              # Noticeably filter motion
    VOCAL_PROCESSING = "vocal_processing"                    # Compression, reverb, delay, autotune


class SongSection(Enum):
    """Standard Hollywood song structure sections"""
    INTRO = "intro"
    VERSE_1 = "verse_1"
    VERSE_CONT = "verse_cont"
    PRE_CHORUS = "pre_chorus"
    CHORUS_1 = "chorus_1"
    VERSE_2 = "verse_2"
    PRE_CHORUS_2 = "pre_chorus_2"
    CHORUS_2 = "chorus_2"
    PRIMARY_BRIDGE = "primary_bridge"
    BRIDGE_CONT = "bridge_cont"
    CHORUS_3 = "chorus_3"
    CHORUS_4 = "chorus_4"
    OUTRO = "outro"


@dataclass
class EnergyPoint:
    """Single point on energy curve"""
    hype: float  # 0-100, abrupt changes
    tension: float  # 0-100, gradual buildup

    @property
    def total_energy(self) -> float:
        """Combine hype and tension for total energy"""
        return (self.hype * 0.6) + (self.tension * 0.4)


@dataclass
class SectionConfig:
    """Configuration for a song section"""
    section: SongSection
    energy_start: EnergyPoint
    energy_end: EnergyPoint
    transition_type: TransitionType
    bars: int  # Number of 8-bar sections
    description: str


class EnergyCurve:
    """Models energy dynamics of a song"""

    def __init__(self, num_peaks: int = 3):
        """
        Initialize energy curve.

        Args:
            num_peaks: Number of energy peaks (typically 3)
        """
        self.num_peaks = num_peaks
        self.points: List[EnergyPoint] = []
        self._generate_hollywood_curve()

    def _generate_hollywood_curve(self):
        """Generate standard 3-act Hollywood energy curve"""
        if self.num_peaks == 3:
            # Classic Hollywood structure
            self.points = [
                EnergyPoint(hype=10, tension=0),    # Intro: lowest energy
                EnergyPoint(hype=30, tension=20),   # Verse 1: building
                EnergyPoint(hype=35, tension=40),   # Pre-chorus: tension rise
                EnergyPoint(hype=60, tension=30),   # Chorus 1: first peak (smaller)
                EnergyPoint(hype=40, tension=50),   # Verse 2: drop + high tension
                EnergyPoint(hype=45, tension=60),   # Pre-chorus 2: more tension
                EnergyPoint(hype=75, tension=40),   # Chorus 2: bigger peak
                EnergyPoint(hype=50, tension=70),   # Bridge: new terrain + tension
                EnergyPoint(hype=55, tension=80),   # Bridge cont: maximum tension
                EnergyPoint(hype=95, tension=50),   # Chorus 3: BIGGEST moment
                EnergyPoint(hype=100, tension=60),  # Chorus 4: finale
                EnergyPoint(hype=20, tension=10),   # Outro: back to status quo
            ]

    def get_energy_at_point(self, index: int) -> EnergyPoint:
        """Get energy at specific point"""
        if 0 <= index < len(self.points):
            return self.points[index]
        return EnergyPoint(hype=50, tension=50)

    def get_total_energy_curve(self) -> List[float]:
        """Get total energy values for all points"""
        return [point.total_energy for point in self.points]

    def is_globally_increasing(self) -> bool:
        """Check if energy generally increases through song (best practice)"""
        first_third = np.mean(self.get_total_energy_curve()[:4])
        last_third = np.mean(self.get_total_energy_curve()[-4:])
        return bool(last_third > first_third)


class CompositionGuide:
    """Generates composition guidance based on Addiction Formula"""

    def __init__(self, genre: str = "pop", energy_curve: Optional[EnergyCurve] = None):
        self.genre = genre.lower()
        self.energy_curve = energy_curve or EnergyCurve()
        self.sections = self._build_section_configs()

    def _build_section_configs(self) -> List[SectionConfig]:
        """Build section configurations with energy guidance"""
        return [
            SectionConfig(
                section=SongSection.INTRO,
                energy_start=EnergyPoint(10, 0),
                energy_end=EnergyPoint(10, 0),
                transition_type=TransitionType.SMOOTH,
                bars=2,
                description="Intro: Set status quo, establish sound, lowest energy point"
            ),
            SectionConfig(
                section=SongSection.VERSE_1,
                energy_start=EnergyPoint(10, 0),
                energy_end=EnergyPoint(30, 30),
                transition_type=TransitionType.SMOOTH,
                bars=4,
                description="Verse 1: Introduce problem, build anticipation gradually"
            ),
            SectionConfig(
                section=SongSection.PRE_CHORUS,
                energy_start=EnergyPoint(30, 30),
                energy_end=EnergyPoint(40, 50),
                transition_type=TransitionType.SMOOTH,
                bars=2,
                description="Pre-chorus: Create tension, pivot to chorus"
            ),
            SectionConfig(
                section=SongSection.CHORUS_1,
                energy_start=EnergyPoint(40, 50),
                energy_end=EnergyPoint(65, 30),
                transition_type=TransitionType.JUMP,
                bars=2,
                description="Chorus 1: First gratification peak - strip elements, don't go too big"
            ),
            SectionConfig(
                section=SongSection.VERSE_2,
                energy_start=EnergyPoint(65, 30),
                energy_end=EnergyPoint(40, 60),
                transition_type=TransitionType.DROP,
                bars=4,
                description="Verse 2: Character development, MUST be bigger than Verse 1"
            ),
            SectionConfig(
                section=SongSection.PRE_CHORUS_2,
                energy_start=EnergyPoint(40, 60),
                energy_end=EnergyPoint(45, 70),
                transition_type=TransitionType.SMOOTH,
                bars=2,
                description="Pre-chorus 2: More energy than first, build to chorus"
            ),
            SectionConfig(
                section=SongSection.CHORUS_2,
                energy_start=EnergyPoint(45, 70),
                energy_end=EnergyPoint(78, 35),
                transition_type=TransitionType.JUMP,
                bars=2,
                description="Chorus 2: Slightly bigger than Chorus 1, add subtle elements"
            ),
            SectionConfig(
                section=SongSection.PRIMARY_BRIDGE,
                energy_start=EnergyPoint(78, 35),
                energy_end=EnergyPoint(50, 80),
                transition_type=TransitionType.SURPRISE,
                bars=4,
                description="Bridge: Explore new terrain, everything changes, maximum tension"
            ),
            SectionConfig(
                section=SongSection.CHORUS_3,
                energy_start=EnergyPoint(50, 80),
                energy_end=EnergyPoint(95, 40),
                transition_type=TransitionType.LIFT,
                bars=2,
                description="Chorus 3: The BIGGEST moment - gratification peak"
            ),
            SectionConfig(
                section=SongSection.CHORUS_4,
                energy_start=EnergyPoint(95, 40),
                energy_end=EnergyPoint(100, 50),
                transition_type=TransitionType.SMOOTH,
                bars=3,
                description="Chorus 4: Finale - go crazy, add elements, highest energy"
            ),
            SectionConfig(
                section=SongSection.OUTRO,
                energy_start=EnergyPoint(100, 50),
                energy_end=EnergyPoint(15, 5),
                transition_type=TransitionType.NEGATIVE_TENSION,
                bars=2,
                description="Outro: Return to status quo, personal note, keep it short"
            ),
        ]

    def get_section_prompt_modifiers(self, section: SongSection) -> dict[str, Any]:
        """Get prompt modifiers for a specific section"""

        base_modifiers = {
            SongSection.INTRO: {
                "energy_level": "minimal",
                "elements": "atmospheric, minimal arrangement",
                "focus": "sound quality over arrangement",
                "tempo_feel": "establishing"
            },
            SongSection.VERSE_1: {
                "energy_level": "low-mid",
                "elements": "sparse, intimate",
                "focus": "narrative, storytelling",
                "tempo_feel": "steady anticipation"
            },
            SongSection.PRE_CHORUS: {
                "energy_level": "building",
                "elements": "increasing percussion, rising melody",
                "focus": "tension, anticipation",
                "tempo_feel": "acceleration"
            },
            SongSection.CHORUS_1: {
                "energy_level": "high",
                "elements": "full arrangement, catchy hook",
                "focus": "gratification, memorable",
                "tempo_feel": "peak energy, driving"
            },
            SongSection.VERSE_2: {
                "energy_level": "mid-high",
                "elements": "richer than verse 1, but not chorus level",
                "focus": "development, moving forward",
                "tempo_feel": "propulsive"
            },
            SongSection.PRIMARY_BRIDGE: {
                "energy_level": "variable",
                "elements": "unexpected sounds, new instrumentation",
                "focus": "contrast, surprise, new direction",
                "tempo_feel": "tension building"
            },
            SongSection.CHORUS_3: {
                "energy_level": "maximum",
                "elements": "all instruments, dense arrangement",
                "focus": "ultimate gratification",
                "tempo_feel": "climax"
            },
            SongSection.CHORUS_4: {
                "energy_level": "sustained maximum",
                "elements": "elements added, solos, variation",
                "focus": "celebration, extension",
                "tempo_feel": "euphoric"
            },
            SongSection.OUTRO: {
                "energy_level": "minimal",
                "elements": "sparse, reflective",
                "focus": "closure, echo of intro",
                "tempo_feel": "fadeout or cold ending"
            },
        }

        return base_modifiers.get(section, {})

    def get_transition_guidance(self, transition: TransitionType) -> dict[str, Any]:
        """Get detailed guidance for executing a transition"""
        guidance_map: dict[TransitionType, dict[str, Any]] = {
            TransitionType.JUMP: {
                "definition": "Abrupt hype increase every 4-8 bars",
                "technique": "Add/remove instruments suddenly without gradual buildup",
                "best_case": "Unexpected, in-your-face, creates chaotic energy",
                "worst_case": "Confusing, show-offy, irritating, draws attention to arrangement",
                "when_to_use": "Verse to verse continuation, bridge continuations (subtle)",
                "difficulty": "Easy - just add instruments",
                "song_examples": "Black Eyed Peas - I Gotta Feeling (jumping at 1:00)",
                "warning": None,
            },
            TransitionType.SMOOTH: {
                "definition": "Gradual energy increase using hype and tension together",
                "technique": "Layer hype increases with rising tension over multiple sections",
                "best_case": "Exciting, anticipatory, beautiful, compelling, has great direction",
                "worst_case": "Can become predictable if overused",
                "when_to_use": "Most common transition, works almost everywhere",
                "difficulty": "Medium - requires balancing hype steps and tension curves",
                "song_examples": "Adele - Set Fire To The Rain (0:55-1:00 build)",
                "warning": "Most popular in hit songs - use to lead into energy peaks",
            },
            TransitionType.DROP: {
                "definition": "Abrupt hype decrease in steps",
                "technique": "Remove instruments suddenly, strip down arrangement",
                "best_case": "Fascinating, surprising, suspenseful",
                "worst_case": "Disappointing, confusing, boring - can lose listeners",
                "when_to_use": "Chorus to verse transitions, needs tension or hook to maintain interest",
                "difficulty": "Tricky - must prevent listener engagement loss",
                "song_examples": "Rihanna - Disturbia (transition at 1:19)",
                "warning": "CRITICAL: Always follow with tension or special hook to keep listeners engaged",
            },
            TransitionType.SURPRISE: {
                "definition": "Build high tension, then drop to lower hype",
                "technique": "Gradually increase tension, then abruptly remove hype",
                "best_case": "Very emotional, gripping, exciting, brutal, intense",
                "worst_case": "Disappointing, confusing, boring",
                "when_to_use": "Chorus to verse, primary bridge transitions",
                "difficulty": "Medium - tension buildup requires precision timing",
                "song_examples": "Usher - Climax (1:14), Katy Perry - Dark Horse (1:17)",
                "warning": "Same risks as regular Drop - ensure engagement doesn't fade",
            },
            TransitionType.OVERSHOOT: {
                "definition": "Build more tension than needed to reach higher hype level",
                "technique": "Over-prepare the listener, then deliver higher energy",
                "best_case": "Can imply underlying turmoil or drama",
                "worst_case": "Disappointing, confusing, boring - listener feels misdirected",
                "when_to_use": "Rare - only when intentional drama is desired",
                "difficulty": "Hard - risky and often backfires",
                "song_examples": "Mark Ronson - Uptown Funk (Bruno Mars, 1:06)",
                "warning": "DANGER: Pretending to go somewhere and not delivering wastes listener goodwill. Avoid unless intentional.",
            },
            TransitionType.FALSE_PROMISE: {
                "definition": "Build high tension but return to same hype level",
                "technique": "Gradually increase tension without hype increases",
                "best_case": "None - this transition is inherently risky",
                "worst_case": "VERY disappointing, boring, confusing, frustrating",
                "when_to_use": "Extreme caution only - use 1 at a time max",
                "difficulty": "Extremely tricky - high risk of listener loss",
                "song_examples": "Usher - Climax, Refused - New Noise (0:47)",
                "warning": "EXTREME DANGER: Even more problematic than Overshoot. Must IMMEDIATELY follow with gratification or implied tension or listener turns off song.",
            },
            TransitionType.FLATLINE: {
                "definition": "Keep hype level unchanged",
                "technique": "Maintain same energy level through the section",
                "best_case": "Works if you have special hook, fantastic vocal, or groovy rhythm",
                "worst_case": "Listener boredom and tune-out",
                "when_to_use": "Ballads, special moments, never as default",
                "difficulty": "Risky - requires exceptional content to hold attention",
                "song_examples": "Taylor Swift - Shake It Off (0:17), Katy Perry - Hot N Cold (0:18)",
                "warning": "When in doubt, always go UP. Flatline kills momentum. Only use if you have something special.",
            },
            TransitionType.LIFT: {
                "definition": "Build less tension than necessary for hype increase",
                "technique": "Jump hype up without extended tension buildup",
                "best_case": "Great direction, moving, huge, powerful punchy entrance",
                "worst_case": "Chaotic, confusing, show-offy, irritating, draws attention",
                "when_to_use": "Into big choruses - creates powerful impact",
                "difficulty": "Medium - requires timing precision",
                "song_examples": "Miley Cyrus - Wrecking Ball (transition at 0:41)",
                "warning": "Packs more punch than Smooth transition - establishes chorus strongly",
            },
            TransitionType.NEGATIVE_TENSION: {
                "definition": "Gradually decrease energy to reach lower hype level",
                "technique": "Remove instruments gradually, reduce filter opening, strip drums",
                "best_case": "Smooth, beautiful, elegant descent",
                "worst_case": "Confusion, disorientation, feeling lost",
                "when_to_use": "Rare - ballads, special moments, intentional emotional drops",
                "difficulty": "Medium - requires careful arrangement planning",
                "song_examples": "Taylor Swift - We Are Never Ever Getting Back Together (1:05)",
                "warning": "Uncommon - most songwriters default to other transitions",
            },
        }
        if transition in guidance_map:
            return guidance_map[transition]
        return {}

    def recommend_transition(self, from_section: SongSection, to_section: SongSection, energy_change: float) -> TransitionType:  # pylint: disable=too-many-return-statements
        """
        Recommend best transition type between two sections.

        Args:
            from_section: Current section
            to_section: Next section
            energy_change: Change in energy (positive = increase, negative = decrease)

        Returns:
            Recommended TransitionType
        """
        # Energy increasing significantly (e.g., verse to chorus)
        if energy_change > 25:
            # Entering a major peak - use Smooth or Lift
            if to_section in [SongSection.CHORUS_1, SongSection.CHORUS_2, SongSection.CHORUS_3, SongSection.CHORUS_4]:
                return TransitionType.LIFT  # Powerful punch into chorus
            return TransitionType.SMOOTH  # Gradual buildup into peaks

        # Energy increasing moderately (e.g., verse to pre-chorus)
        if energy_change > 10:
            return TransitionType.SMOOTH  # Gradual increase

        # Energy decreasing significantly (e.g., chorus to verse)
        if energy_change < -25:
            # Dropping back after peak - use Surprise for drama or Drop for simplicity
            if from_section in [SongSection.CHORUS_1, SongSection.CHORUS_2, SongSection.CHORUS_3, SongSection.CHORUS_4]:
                return TransitionType.SURPRISE  # Build tension under the drop
            return TransitionType.DROP  # Simple strip-down

        # Energy decreasing moderately
        if energy_change < -10:
            return TransitionType.NEGATIVE_TENSION  # Smooth decrease

        # Energy staying relatively flat
        # Same energy level - use Jump or Flatline
        if from_section == SongSection.VERSE_1 and to_section == SongSection.VERSE_CONT:
            return TransitionType.JUMP  # Subtle step up
        return TransitionType.JUMP  # Add subtle variation

    def recommend_buildup_technique(self, target_energy_peak: EnergyPoint, current_energy: EnergyPoint) -> BuildUpTechnique:
        """
        Recommend how to build up to a peak.

        Args:
            target_energy_peak: Target energy point
            current_energy: Starting energy point

        Returns:
            Recommended BuildUpTechnique
        """
        hype_delta = target_energy_peak.hype - current_energy.hype
        tension_delta = target_energy_peak.tension - current_energy.tension

        # Major hype jump needed (every 4-8 bars) - use combined
        if hype_delta > 20:
            if tension_delta > 15:
                return BuildUpTechnique.COMBINED  # Most effective
            return BuildUpTechnique.HYPE_ONLY  # Abrupt, chaotic effect

        # Moderate hype increase - use combined
        if hype_delta > 10:
            return BuildUpTechnique.COMBINED

        # High tension needed but low hype - use tension only
        if tension_delta > 20 and hype_delta < 5:
            return BuildUpTechnique.TENSION_ONLY  # Smooth, mysterious buildup

        # Default - use combined for most flexibility
        return BuildUpTechnique.COMBINED

    def validate_energy_curve_rules(self, curve: 'EnergyCurve') -> dict[str, bool | list[str]]:
        """
        Validate energy curve against Addiction Formula principles.

        Returns:
            Dict with validation results and recommendations
        """
        passes = True
        issues: list[str] = []
        recommendations: list[str] = []

        energies = curve.get_total_energy_curve()

        # Rule 1: Overall energy should increase
        if not curve.is_globally_increasing():
            passes = False
            issues.append("Overall energy does not increase - violates key principle")
            recommendations.append("Make Verse 2 bigger than Verse 1, and Chorus 2 bigger than Chorus 1")

        # Rule 2: Biggest peak should be in last third
        max_energy_idx = energies.index(max(energies))
        if max_energy_idx < len(energies) * 0.6:
            passes = False
            issues.append("Biggest energy peak not in final third of song")
            recommendations.append("Move climax (Chorus 3/4) to end, make it bigger than earlier peaks")

        # Rule 3: Check for false promises (tension spike then drop at same hype)
        for i in range(len(curve.points) - 1):
            if curve.points[i].tension > 50 and curve.points[i+1].tension < 30:
                if abs(curve.points[i].hype - curve.points[i+1].hype) < 10:
                    recommendations.append(
                        f"Point {i} → {i+1}: Tension spike without hype increase detected (False Promise risk) - "
                        "follow with immediate gratification to avoid listener frustration"
                    )

        # Rule 4: Check 1-2-3 rule adherence
        # Look for sufficient variety in energy values
        energy_diffs = [abs(energies[i] - energies[i-1]) for i in range(1, len(energies))]
        avg_diff = sum(energy_diffs) / len(energy_diffs)
        if avg_diff < 5:
            recommendations.append("Energy curve is too flat - increase variation between sections for better 1-2-3 rule adherence")

        return {
            "passes": passes,
            "issues": issues,
            "recommendations": recommendations,
        }

    def get_section_transition_strategy(
        self,
        from_section: SongSection,
        to_section: SongSection,
    ) -> dict[str, Any]:
        """
        Get detailed transition strategy between two sections.

        Returns:
            Dict with transition type, technique, and specific guidance
        """
        from_config = next((s for s in self.sections if s.section == from_section), None)
        to_config = next((s for s in self.sections if s.section == to_section), None)

        if not from_config or not to_config:
            return {}

        energy_change = to_config.energy_end.total_energy - from_config.energy_end.total_energy
        transition_type = self.recommend_transition(from_section, to_section, energy_change)
        buildup_technique = self.recommend_buildup_technique(to_config.energy_end, from_config.energy_end)

        transition_detail = self.get_transition_guidance(transition_type)

        return {
            "from_section": from_section.value,
            "to_section": to_section.value,
            "energy_change": energy_change,
            "transition_type": transition_type.value,
            "transition_detail": transition_detail,
            "buildup_technique": buildup_technique.value,
            "specific_guidance": self._get_specific_guidance(from_section, to_section, transition_type),
        }

    def _get_specific_guidance(self, from_section: SongSection, to_section: SongSection, transition_type: TransitionType) -> str:
        """Get specific guidance for common section transitions"""
        guidance_map = {
            (SongSection.VERSE_1, SongSection.PRE_CHORUS):
                "Build tension gradually over 8 bars. Use hype increases every 4-8 bars plus rising tension.",
            (SongSection.PRE_CHORUS, SongSection.CHORUS_1):
                "This is the first reward moment. Use LIFT transition for powerful entrance into chorus.",
            (SongSection.CHORUS_1, SongSection.VERSE_2):
                "You're dropping energy - this is risky. Use SURPRISE (build tension while dropping hype) to prevent listener loss.",
            (SongSection.VERSE_2, SongSection.PRE_CHORUS_2):
                "Verse 2 MUST be bigger than Verse 1. Build with both hype steps AND rising tension.",
            (SongSection.CHORUS_2, SongSection.PRIMARY_BRIDGE):
                "Bridge is new territory. Can use JUMP or DROP to signal change. Keep listener engaged with surprise elements.",
            (SongSection.PRIMARY_BRIDGE, SongSection.CHORUS_3):
                "CLIMAX moment! Use LIFT for maximum impact. This should be THE biggest moment in the song.",
            (SongSection.CHORUS_3, SongSection.CHORUS_4):
                "Sustain euphoria with variations. Use JUMP to add new elements or keep hype high.",
            (SongSection.CHORUS_4, SongSection.OUTRO):
                "Return to status quo. Use NEGATIVE_TENSION to gradually fade out, or DROP for sudden ending.",
        }

        key = (from_section, to_section)
        return guidance_map.get(key, "Transition executed with " + transition_type.value)


class ElementGuidance:
    """Guidance for the six songwriting elements"""

    @staticmethod
    def get_arrangement_guidance(_tension_type: TensionType) -> dict[TensionType, dict[str, str]]:
        """Get arrangement-specific guidance"""
        return {
            TensionType.REGULAR: {
                "for_hype": "Fuller texture = higher hype. Add/remove instruments every 4-8 bars for direction.",
                "technique": "Layer instruments gradually or remove them to create "
                              "blocky energy changes",
                "example": "Verse: bass + guitar. Pre-chorus: add strings. Chorus: full arrangement (highs, mids, lows)",
            },
            TensionType.IMPLIED: {
                "definition": "Noticeably strip elements to create absence that "
                              "pulls listener forward",
                "technique": "Remove bass, kick drum, snare, hi-hat, or vocals "
                              "mid-section to hint at next energy",
                "best_for": "Dropping from high energy while maintaining engagement (Drop → Verse transitions)",
                "example": "After chorus: remove bass drum and bass, keep vocals "
                            "+ pads. Listener feels something missing.",
                "critical": "Must be NOTICEABLE. If it's just a regular energy drop, you've failed.",
            }
        }

    @staticmethod
    def get_harmony_guidance(_harmony_tension: HarmonyTension) -> dict[HarmonyTension, dict[str, str]]:
        """Get harmony-specific guidance by chord category"""
        return {
            HarmonyTension.TONIC: {
                "tension_level": "LOW - No natural tension",
                "chords_major": "I, vi, iii",
                "chords_minor": "i, VI, III",
                "use_for": "Verses, safe sections, grounding moments",
                "strategy": "Combine with rhythm or arrangement tension to "
                            "create anticipation",
            },
            HarmonyTension.SUBDOMINANT: {
                "tension_level": "MEDIUM - Some tension",
                "chords_major": "IV, ii, II",
                "chords_minor": "iv, IV",
                "use_for": "Pre-chorus, bridge setup, mid-section builds",
                "strategy": "Good for moving toward dominant sections",
            },
            HarmonyTension.DOMINANT: {
                "tension_level": "HIGH - Maximum tension",
                "chords_major": "V, bVII",
                "chords_minor": "V, VII, bII, v",
                "use_for": "Pre-chorus climax, bridge tension, just before chorus",
                "strategy": "Create pull toward resolution (typically back to "
                            "tonic or chorus)",
                "technique": "Listen to 12-bar blues (I-I-I-I, IV-IV-I-I, "
                              "V-IV-I-V) to internalize the difference",
            }
        }

    @staticmethod
    def get_rhythm_guidance(_subdivision: RhythmicSubdivision) -> dict[RhythmicSubdivision, dict[str, str]]:
        """Get rhythm-specific guidance by subdivision"""
        return {
            RhythmicSubdivision.WHOLE: {
                "hype_level": "LOWEST",
                "use_for": "Intro, minimalist moments, slow ballads",
                "example": "One note held whole song intro",
            },
            RhythmicSubdivision.HALF: {
                "hype_level": "LOW",
                "use_for": "Verses with sparse rhythm",
                "example": "Half-note hi-hat patterns",
            },
            RhythmicSubdivision.QUARTER: {
                "hype_level": "MEDIUM",
                "use_for": "Standard verse rhythm (4-on-floor beat)",
                "example": "Quarter-note kick drum pattern",
            },
            RhythmicSubdivision.EIGHTH: {
                "hype_level": "HIGH",
                "use_for": "Chorus rhythm, more energy than verse",
                "example": "Eighth-note hi-hat, busier drum pattern",
            },
            RhythmicSubdivision.SIXTEENTH: {
                "hype_level": "HIGHEST",
                "use_for": "Pre-chorus builds, climactic moments",
                "example": "Sixteenth-note hi-hat rolls, trap-style hi-hats",
                "tension_strategy": "Introduce sub16 in sub8 section for immediate energy boost (tension through subdivision change)",
            }
        }

    @staticmethod
    def get_vocal_guidance() -> dict[str, Any]:
        """Comprehensive vocal technique guidance based on The Addiction Formula vocals chapter.

        Key insight: All instruments that create hit songs share one characteristic -
        closeness to the human voice. Vocals are where listeners focus their attention.
        """
        return {
            "master_principle": {
                "vocal_centrality": "Humans naturally focus on the human voice. Use vocals strategically - best placement = highest engagement.",
                "why_vocals_dominate": "Wah-wah guitar mimics 'wow', dubstep bass mimics angry 'WHAT', saxophone is closest to vocal timbre, trumpet with harmon mute mimics laughter.",
                "violin_parallel": "Spectral analysis shows violin sonically identical to classical soprano - closeness to voice matters.",
                "practical_rule": "For maximum energy, keep vocals present in every section. Example: Katy Perry's Dark Horse has vocals (including background 'hey's) in every single section including instrumental interludes.",
            },

            "hype_control_range": {
                "principle": "Pitch determines hype: higher pitch = higher hype, lower pitch = lower hype",
                "structure_pattern": "Most hit songs have highest notes in chorus and lowest in verse",
                "implementation": "Verse vocal in low range → Pre-chorus in mid range → Chorus in highest range",
                "power_of_pitch": "Pitch change is one of the most direct hype controls available",
            },

            "hype_control_variety": {
                "principle": "More melodic variety = higher hype. One-note melody = lowest hype possible",
                "one_note_use": "One-note melodies save energy for lyrics or create monotone effect",
                "variety_maximum": "Chorus with many different notes = high hype",
                "example_contrast": "Lady Gaga Poker Face: one-note verses (limited pitch) vs many-note choruses (high variety)",
            },

            "vocal_modes_detailed": {
                VocalMode.SPEECH.value: {
                    "hype_level": "LOWEST (varies with pitch)",
                    "characteristics": "Conversational, rap-like, relatable, intimate",
                    "use_for": "Verses, rap sections, conversational moments",
                    "power_note": "Low-energy but direct engagement through relatability",
                    "examples": "Ke$ha TiK ToK (chorus - conversational delivery), Katy Perry E.T. (verse - speech-like)",
                },
                VocalMode.NEUTRAL.value: {
                    "hype_level": "LOW-MEDIUM (natural singing)",
                    "characteristics": "Natural singing voice, organic, safe, versatile",
                    "use_for": "Verses, flexible use throughout",
                    "power_note": "Most widely usable mode, foundation for other modes",
                    "examples": "John Legend All Of Me (1:32-1:43 neutral high), OneRepublic Counting Stars (verse low)",
                },
                VocalMode.FALSETTO.value: {
                    "hype_level": "MEDIUM-HIGH (with air/lightness)",
                    "characteristics": "Light, airy, ethereal, surprising contrast, emotional",
                    "use_for": "Pre-chorus peaks, contrast moments, emotional builds",
                    "power_note": "Creates surprise when switching from neutral/speech",
                    "examples": "Katy Perry E.T. (pre-chorus), Dark Horse (pre-chorus at 0:34)",
                },
                VocalMode.BELTING.value: {
                    "hype_level": "HIGHEST (projected power)",
                    "characteristics": "Powerful, emotional, projected, requires 'edge', high intensity",
                    "use_for": "Chorus peaks, climactic moments, maximum energy",
                    "power_note": "Strongest hype state, but cannot be sustained continuously",
                    "examples": "Miley Cyrus Wrecking Ball (chorus), Sia Chandelier (chorus)",
                    "requirement": "Belting inherently requires twang to protect voice",
                },
            },

            "vocal_effects_comprehensive": {
                VocalEffect.TWANG.value: {
                    "definition": "Adding oral and nasal resonance to the voice",
                    "hype_effect": "Raises hype when applied",
                    "typical_context": "High-energy sections, choruses, mandatory with belting",
                    "strategy": "Add gradually from verse through pre-chorus for tension effect",
                    "examples": "Lady Gaga Bad Romance (twang enters at 0:17), Pink Raise Your Glass (twang in chorus)",
                    "note": "Twang is not optional with belting - it's a requirement",
                },
                VocalEffect.VIBRATO.value: {
                    "definition": "Rhythmic oscillation on held notes",
                    "hype_effect": "Adds rhythmic pulses (raises hype) and adds interest",
                    "typical_context": "Ballads, long held notes, emotional moments",
                    "modern_context": "Less common in contemporary pop (risks sounding 'Freddy Mercury')",
                    "strategy": "Slow vibrato = controlled emotion. Fast vibrato = more energy",
                    "examples": "Beyoncé If I Were A Boy, John Legend All Of Me",
                },
                VocalEffect.ORNAMENTATIONS.value: {
                    "definition": "Very fast, rhythmic, melodic sequences of notes (RnB runs)",
                    "hype_effect": "Increases sung pitches (variety) and rhythmic activity (both raise hype)",
                    "typical_context": "RnB, soul, high-energy sections",
                    "strategy": "Adds complexity and engagement through rapid melodic movement",
                    "examples": "Ariana Grande Problem ft. Iggy Azalea (2:46-end with runs)",
                },
                VocalEffect.DISTORTION.value: {
                    "definition": "Adding aggression/edge to the voice, classified by pitch",
                    "types_ranked": {
                        VocalDistortionType.GROWLING.value: "Low pitch - lowest hype in distortion family",
                        VocalDistortionType.SHOUTING.value: "Mid-range pitch - medium distortion hype",
                        VocalDistortionType.SCREAMING.value: "High pitch - highest distortion hype",
                        VocalDistortionType.CURBING.value: "Very subtle - used in pop, alternative rock",
                    },
                    "typical_context": "Rock, metal, aggressive emotional moments",
                    "typical_context_pop": "Very subtle forms only (known as 'curbing')",
                    "examples": "Nickelback How You Remind Me (subtle curbing), Linkin Park One Step Closer (2:06 screaming)",
                },
            },

            "creating_tension_five_ways": {
                VocalTensionTechnique.ASCENDING_MELODY.value: {
                    "method": "Write melodies that gradually rise in pitch across a section",
                    "effect": "Pitch rise creates natural anticipation toward next section",
                    "timing": "Sustained across 4-8 bars or one full section",
                    "examples": "Katy Perry Firework (0:39-0:54), Ariana Grande Problem (0:30-0:39)",
                },
                VocalTensionTechnique.MODE_SHIFT.value: {
                    "method": "Change to higher-hype vocal mode mid-section",
                    "effect": "Immediate hype increase while staying on same pitches",
                    "timing": "Usually at bridge of section or start of pre-chorus",
                    "examples": "Katy Perry Dark Horse (0:34: falsetto to neutral), Fall Out Boy Dance Dance (0:39: neutral to belting)",
                },
                VocalTensionTechnique.POWER_INCREASE.value: {
                    "method": "Singer gradually increases emotional power/intensity mid-section",
                    "effect": "Builds toward peak without pitch or mode change",
                    "timing": "Slow crescendo across 4-8 bars",
                    "examples": "Natasha Bedingfield Soulmate (2:16: slow power increase)",
                },
                VocalTensionTechnique.TENSE_NOTES.value: {
                    "method": "Hit specific tense notes: 3rd or 7th of V chord at section end",
                    "effect": "Harmonic tension highlighted through vocal note selection",
                    "warning": "Immediately sounds classical/clichéd - rarely used in modern pop",
                    "context": "Educational technique, not mainstream application",
                },
                VocalTensionTechnique.EFFECT_CRESCENDO.value: {
                    "method": "Gradually add effects (twang, distortion) leading to peak",
                    "effect": "Signals movement to higher-energy section through effect layering",
                    "timing": "Start subtle, increase intensity over 2-4 bars",
                    "examples": "Pink Raise Your Glass (1:32: twang starts, then distortion), Clean Bandit Rather Be (3:07: twang)",
                },
            },

            "creating_implied_tension_four_ways": {
                VocalImpliedTensionTechnique.SUBTRACT_MELODY.value: {
                    "definition": "Remove vocals entirely, creating noticeable absence",
                    "effect": "Listeners feel vocal presence missing, anticipate return",
                    "timing": "Most popular: right before chorus (end of pre-chorus)",
                    "power": "Extremely impactful because vocals get most attention",
                    "examples": "Lady Gaga Applause (0:53: vocals drop before chorus)",
                },
                VocalImpliedTensionTechnique.TENSE_ONE_NOTE.value: {
                    "definition": "One-note melody on note NOT in your tonic triad",
                    "effect": "Creates friction between vocal and harmony that wants to resolve",
                    "example_technique": "If home chord is C major, sing G (5th, not in C-E-G triad) continuously",
                    "examples": "Justin Timberlake Pose (verses on #11), Janelle Monáe Tightrope (verses on b7)",
                },
                VocalImpliedTensionTechnique.SPACE.value: {
                    "definition": "Use breathing/rests between vocal lines (not continuous singing)",
                    "effect": "Allows music to shine through, creates tension through absence",
                    "contrast_problem": "'Lyrical chains' (continuous text blocks) destroy tension - common songwriter mistake",
                    "solution": "Say what needs saying in fewest words possible - let melody breathe",
                    "mastery_key": "Singer must turn rests into space (requires breath/tension control in voice)",
                    "technique": "Sing lyrics in blocks, not line-by-line - creates natural breathing points",
                    "examples": "Bryan Adams Where Angels Fear To Tread (masterful space), Inside Out (minimal lyrics, maximum breathing)",
                    "exercise": "Take a verse from sad ballad, add more words - you'll feel how it destroys tension. Subtract words = more tension.",
                },
                VocalImpliedTensionTechnique.ATTITUDE_CONTRAST.value: {
                    "definition": "Contrast energy between vocals and backing music",
                    "scenario_one": "Low-energy vocal delivery over high-energy music = powerlessness, depression, apathy, boredom",
                    "scenario_two": "High-energy vocal over low-energy music = emotional ballad, vocal ability showcase",
                    "effect": "Creates psychological tension through expectation mismatch",
                    "examples": "Stromae Alors On Danse (low-energy vocal over dance beat = depression), The Cranberries Zombie (low-energy over intense music)",
                },
            },

            "vocal_melody_variety_control": {
                "one_note_lowest": "Single repeated note = lowest hype possible",
                "limited_notes": "3-5 different notes in section = verse-level hype",
                "medium_variety": "7-10 different notes = chorus-capable hype",
                "high_variety": "15+ different notes with large range jumps = peak energy",
            },

            "vocal_distance_from_home": {
                "principle": "One-note melody on tonic note (home) = no tension. Same melody on non-tonic = creates friction.",
                "harmony_awareness": "Singers should know tonic triad (I chord: root, 3rd, 5th)",
                "tension_formula": "Melody note OUTSIDE tonic triad + harmonic support = implied tension waiting for resolution",
            },

            "practical_structure": {
                "typical_verse": "Lower pitch range, speech or neutral mode, limited melodic variety, with space/breathing",
                "typical_pre_chorus": "Mid-high pitch, falsetto or neutral shift, ascending melody, building toward chorus",
                "typical_chorus": "Highest pitch, belting or powerful neutral, wide melodic variety, continuous energy without space",
                "typical_bridge": "Often uses contrast - could be lower energy, different vocal mode, or attitude contrast",
            },
        }

    @staticmethod
    def get_lyrics_guidance() -> dict[str, Any]:
        """Comprehensive lyric technique guidance.

        Key principle: Lyrics are NOT separate from music - they're another instrument.
        Music and lyrics must follow the same energy curve or they won't fit together.
        """
        return {
            "master_principle": {
                "lyrics_as_instrument": "Treat lyrics as you would any other instrument - a tool to control energy curve",
                "synchronization": "Music and lyrics MUST follow same energy curve - mismatched hype between them creates jarring dissonance",
                "pareto_principle": "20% of your lyrics (power words in power positions) create 80% of impact - focus effort there",
                "specificity": "Verses should be specific/detailed. Choruses should be big-picture/interpretable.",
            },

            "power_positions": {
                "principle": "Certain moments give lyrical lines higher status due to song structure (1-2-3 rule)",
                "most_powerful": "First line of primary bridge / Last line of second chorus (3 nodes = highest value)",
                "very_powerful": "Very first line of song AND very last line of song (2 nodes each = memorable)",
                "strategy": "Identify power positions in your structure, place strongest lines there",
                "hollywood_positions": [
                    "First line of first verse",
                    "Last line of first verse / First line of pre-chorus",
                    "Last line of pre-chorus / First line of chorus",
                    "Last line of chorus / First line of second verse",
                    "Last line of second chorus / First line of bridge",
                    "Last line of bridge / First line of third chorus",
                    "Last line of final chorus"
                ]
            },

            "hype_control": {
                "scope": {
                    "specific_low_hype": "Detailed descriptions, what you see/feel, story details, go into detail",
                    "general_high_hype": "Big picture, explanations, summaries, revelations, meta-commentary",
                    "strategy": "Use specificity in verses, expand scope in choruses"
                },
                "power_words": {
                    "definition": "Words evoking strong emotional reaction or carrying deeper meaning",
                    "effect": "Raise hype and memorability significantly",
                    "application": "Place in power positions, spend extra time crafting these",
                    "types": "Emotionally charged, metaphorical, reflective of artist image, zeitgeist-relevant"
                }
            },

            "tension_contentual": {
                "story_progression": "Continuous narrative building across verse 1 → verse 2 → bridge",
                "cliffhanger_question": "End section with unanswered question creating interest",
                "cliffhanger_surprise": "End section with unexpected revelation (high tension)",
                "cliffhanger_cutoff": "Cut off chain of events at climactic moment (makes audience anticipate continuation)"
            },

            "tension_structural": {
                "pickup": "Vocal line enters before section boundary - creates anticipation",
                "split_line": "Line split across section boundary with pause - audience waits for completion",
                "ouroboros_melody": "Lyrical blocks misaligned with musical sections - creates dovetailing effect (rare, sophisticated)"
            },

            "implied_tension_contentual": {
                "low_energy_lyrics_high_energy_music": "Creates powerlessness, depression, apathy, boredom feeling",
                "high_energy_lyrics_low_energy_music": "Creates emotional intensity, vocal showcase effect"
            },

            "implied_tension_structural": {
                "asymmetric_phrasing": "Write 3 or 5 line blocks instead of standard 4 - breaks predictability",
                "internal_split_lines": "Take pauses mid-line within section (not crossing boundaries) - creates tension within moment",
                "break_block_predictability": "Avoid standard 'one line every two bars' - write more freely over section"
            },

            "section_specific_guidance": {
                LyricSectionRole.INTRO.value: "Establish mood, introduce vocals early, brief improvisation acceptable",
                LyricSectionRole.FIRST_VERSE.value: "Power position - introduce characters, be specific, grab immediate attention",
                LyricSectionRole.PRE_CHORUS.value: "One-two lines leading to chorus, introduce inciting incident if not in verse",
                LyricSectionRole.CHORUS.value: "Multi-faceted, big-picture, invite multiple interpretations, no time for details",
                LyricSectionRole.SECOND_VERSE.value: "Deepen story, zoom out to bigger perspective, establish higher energy than verse 1",
                LyricSectionRole.BRIDGE.value: "Surprise element - change writing technique, plot turn, new perspective",
                LyricSectionRole.FINAL_CHORUS.value: "Drive point home, reinforce message, make it memorable",
                LyricSectionRole.OUTRO.value: "Return to intro mood OR sustain high energy - match your ending strategy"
            },

            "verse_vs_chorus_philosophy": {
                "verse_goal": "Make listener believe your story - go into detail, be specific about your life",
                "chorus_goal": "Create 3D depth through multiple valid interpretations - bigger scope allows more meaning",
                "interpretation_power": "More interpretations = song reaches more people in different life situations"
            }
        }

    @staticmethod
    def get_production_guidance() -> dict[str, Any]:
        """Comprehensive production technique guidance for creative sound design.

        Key principle: Production is about creative effect choices to tell story and ride energy curve.
        This is NOT mixing/mastering technique - it's sound design as songwriting element.
        """
        return {
            "master_principle": {
                "production_as_songwriting": "Production is a songwriting element - use effects to tell story like any other instrument",
                "sound_design_era": "Modern songwriting merges writing with production - sound design is essential",
                "piano_test_obsolete": "Old rule 'song works on piano' no longer applies - production is integral",
                "creative_control": "Producer has most control of any element - ideal for subtle implied tension techniques"
            },

            "hype_setting_methods": {
                ProductionHypeMethod.FATTENING.value: {
                    "techniques": "Layering, compression, filters, chorus effects, distortion",
                    "principle": "Thicker = higher hype. More density in mix = more energy",
                    "application": "Add layers gradually moving toward chorus"
                },
                ProductionHypeMethod.THINNING.value: {
                    "techniques": "Remove layers, reduce compression, open filters",
                    "principle": "Thinner = lower hype. Sparse mix = less energy",
                    "application": "Strip down for verses, build for choruses"
                },
                ProductionHypeMethod.PERCEIVED_VOLUME.value: {
                    "techniques": "Compression, volume automation, dynamic range control",
                    "principle": "Perceived loudness increases hype independent of actual volume",
                    "application": "Pull verses down a few dB to give chorus lift"
                },
                ProductionHypeMethod.DIMENSION_SPACE.value: {
                    "techniques": "Stereo widening, reverb, delay, spatial effects",
                    "principle": "Wider and closer = higher hype. Space is relative - need dry/wet contrast",
                    "application": "Keep some elements dry (close) and some wet (distant) for depth"
                },
                ProductionHypeMethod.NEW_INSTRUMENTS.value: {
                    "techniques": "Add pads, percussion, synths, samples mid-section",
                    "principle": "New instruments increase hype through texture expansion",
                    "warning": "Adding instruments to verses for beauty also raises hype - check in context"
                },
                ProductionHypeMethod.PROCESSING.value: {
                    "techniques": "Any noticeable effect becomes hype raiser",
                    "principle": "Noticeable effects signal energy increase",
                    "examples": "Glitchy effects, distortion, modulated delays, wobble bass (LFO)"
                }
            },

            "tension_creation": {
                "automation_strategy": "Automation is KEY - gradually change parameters to lead through energy curve",
                ProductionTensionMethod.AUTOMATION_FATTENING.value: "Fade in layers, gradually increase compression, slowly open filters",
                ProductionTensionMethod.AUTOMATION_FILTER.value: "Gradually change cutoff frequency - automate the resonance",
                ProductionTensionMethod.AUTOMATION_VOLUME.value: "Volume crescendo - mimics crescendo on any instrument",
                ProductionTensionMethod.AUTOMATION_SPACE.value: "Gradually add reverb/delay - open up the space",
                ProductionTensionMethod.AUTOMATION_EFFECTS.value: "Gradually add/increase effects - signals movement to higher energy",
                ProductionTensionMethod.SOUND_EFFECT_UPLIFTER.value: "Rising white noise sweep - common in modern pop for build moments",
                ProductionTensionMethod.SOUND_EFFECT_DOWNLIFTER.value: "Falling sweep - create negative tension or drop effect",
                ProductionTensionMethod.SOUND_EFFECT_WHOOSH.value: "Transition sweeps - directional movement through space",
                ProductionTensionMethod.SOUND_EFFECT_REVERSE.value: "Reversed audio - creates anticipation and movement"
            },

            "implied_tension_production": {
                "principle": "Production is ideal for subtle implied tension - most control of any element",
                ProductionImpliedTensionMethod.HIGHPASS_FILTER.value: "Audibly thin out high end - noticeably missing frequencies",
                ProductionImpliedTensionMethod.LOWPASS_FILTER.value: "Audibly dull low end - frequencies cut off creates incompleteness",
                ProductionImpliedTensionMethod.AUTO_FILTER.value: "Noticeable filter motion - listeners hear filtering happening",
                ProductionImpliedTensionMethod.VOCAL_PROCESSING.value: "Subtle processing differences - compression, reverb, delay, autotune creates subconscious tension from expectation mismatch"
            },

            "practical_workflow": {
                "start_with": "Sound design for effect types - collect sounds for common uses",
                "build_library": "Organize uplifters, downlifters, whooshes, sweeps in folders for drag-and-drop",
                "automate_everything": "Look at energy curve and automate parameters to match",
                "check_context": "Always listen added instruments/effects IN CONTEXT with full song - hype changes in context"
            }
        }

    @staticmethod
    def get_power_positions_analysis(_song_structure: dict[str, Any]) -> dict[str, str]:
        """Analyze power positions in a given song structure using 1-2-3 rule"""
        return {
            "methodology": "Golden Mean (1-2-3 rule): Introduce something, repeat, then change = creates power moments",
            "power_positions": "Positions marking introduction/change always get more attention and memorability",
            "application": "Place strongest lyrical lines at these critical structural moments",
            "most_powerful": "Position with highest node coincidence (where 2-3 structural changes overlap)"
        }

    @staticmethod
    def get_ten_step_songwriting_formula() -> list[dict[str, str | int]]:
        """The Addiction Formula 10-step process for writing addictive songs"""
        return [
            {
                "step": 1,
                "action": "Write A Section",
                "method": "Don't overthink - play chords, find melody, record to click, add instruments"
            },
            {
                "step": 2,
                "action": "Determine What You Have",
                "method": "Identify if it's chorus, verse, bridge, intro, or riff based on energy characteristics"
            },
            {
                "step": 3,
                "action": "Find Your Energy Curve",
                "method": "Sketch compelling energy curve on paper - commit to visual representation of story"
            },
            {
                "step": 4,
                "action": "Make A Rough Outline",
                "method": "Set markers for each section (start 8 bars each), copy/paste section to positions, write others following specifications"
            },
            {
                "step": 5,
                "action": "Set Hype Levels",
                "method": "Check each section against energy curve target - strip/add instruments to match hype"
            },
            {
                "step": 6,
                "action": "Introduce Tension",
                "method": "Add transitions between sections - use tension techniques matching your energy curve"
            },
            {
                "step": 7,
                "action": "Play With Implied Tension",
                "method": "Mute tracks to test implied tension effects - section "
                           "can go down in hype if implied tension works"
            },
            {
                "step": 8,
                "action": "(S)hit Test #1: Friend Test",
                "method": "Send to friends (musicians and non-musicians), collect "
                           "feedback, rewrite critical sections if feedback resonates"
            },
            {
                "step": 9,
                "action": "(S)hit Test #2: Moving Boreders",
                "method": "Listen as if first time (after day rest), identify "
                           "bored-line, move it back through hype/tension techniques"
            },
            {
                "step": 10,
                "action": "Release & Learn",
                "method": "Use analytics to identify problem zones, collect feedback, "
                           "learn for next songs"
            }
        ]

    @staticmethod
    def get_bored_line_analysis() -> dict[str, Any]:
        """Moving Boreders concept - identify where audience loses interest"""
        return {
            "bored_line_definition": "Moment when listener changes station - when they feel they've heard what they needed to hear",
            "typical_bad_song": "Around 15 seconds (when vocals enter) or ~1:15 (when verse 2 hits)",
            "identification_methods": [
                "Listen to song as if first time (requires fresh ears - wait day or two)",
                "Recreate 'fresh listen' by bouncing track, listening in new context",
                "Ask friend to draw energy curve - if different from yours, bored-line likely earlier",
                "Check YouTube analytics - average watch duration shows actual bored-line"
            ],
            "why_bored_line_happens": [
                "Not giving audience enough reasons to keep listening",
                "Listener dislikes an element (vocals, production, or style mismatch)",
                "Listener confused - can't follow the story"
            ],
            "fixing_bored_line": [
                "Move bored-line back through arrangement increases (more hype)",
                "Move bored-line back through tension techniques (anticipation building)",
                "Shorten song ('kill your babies') if it goes beyond 4 minutes",
                "Common fixes: shorten second verse or bridge"
            ],
            "goal": "Move bored-line all the way past song ending if possible"
        }

    @staticmethod
    def get_element_power_ranking() -> list[tuple[str, str]]:
        """Elements ranked by their power to affect energy (most to least powerful)"""
        return [
            ("Arrangement", "Most powerful - texture & instrumentation dominates energy perception"),
            ("Rhythm", "Rhythm (especially subdivisions) is primary tension generator"),
            ("Harmony", "Harmonic movement creates directional pull"),
            ("Part-Writing", "Individual instrument lines and dynamics"),
            ("Production", "Effects, filters, mixing details"),
            ("Lyrics", "Least powerful for energy, but critical for meaning"),
        ]

    @staticmethod
    def get_six_element_communication_model() -> dict[str, Any]:
        """The communication chain: Thought → Encryption → Decryption → Feeling"""
        return {
            "your_side": {
                "step1_thought": "The story/energy curve you want to tell",
                "step2_encryption": "The 6 songwriting elements (arrangement, harmony, rhythm, part-writing, lyrics, production)",
            },
            "their_side": {
                "step3_decryption": "How audience perceives/understands your song",
                "step4_feeling": "How they feel about it (like/dislike, engage/tune-out)",
            },
            "success_criterion": "If listener could draw your energy curve after listening, you encrypted successfully",
            "failure_mode": "If listener draws different/less beautiful curve, you failed the encryption",
            "key_principle": "Control steps 1-2 well, step 3 (decryption) takes care of itself",
        }


class GratificationScorer:
    """Scores how well a composition follows Addiction Formula principles"""

    @staticmethod
    def score_energy_progression(energy_curve: EnergyCurve) -> float:
        """Score if energy generally increases (0-100)"""
        energies = energy_curve.get_total_energy_curve()
        if len(energies) < 2:
            return 0

        first_half = np.mean(energies[:len(energies)//2])
        second_half = np.mean(energies[len(energies)//2:])

        # Score: how much does second half exceed first half
        progression = (second_half - first_half) / 100 * 100
        return float(max(0, min(100, progression)))

    @staticmethod
    def score_peak_placement(energy_curve: EnergyCurve) -> float:
        """Score if biggest peak is at the end (0-100)"""
        energies = energy_curve.get_total_energy_curve()
        if len(energies) < 2:
            return 0

        max_energy = max(energies)
        max_index = energies.index(max_energy)

        # Score is higher if max is in last third
        if max_index >= len(energies) * 0.6:
            return 100
        if max_index >= len(energies) * 0.4:
            return 50
        return 10

    @staticmethod
    def score_variety_vs_repetition(energy_curve: EnergyCurve) -> float:
        """Score balance of repetition and change (0-100)"""
        energies = energy_curve.get_total_energy_curve()
        if len(energies) < 3:
            return 50

        # Check for 1-2-3 pattern (introduce, repeat, change)
        # Too much repetition = boring, too much change = chaotic
        diffs = [abs(energies[i] - energies[i-1]) for i in range(1, len(energies))]
        avg_diff = np.mean(diffs)

        # Optimal: moderate changes
        if 10 < avg_diff < 30:
            return 100
        if 5 < avg_diff < 40:
            return 75
        return 40

    @staticmethod
    def score_composition(energy_curve: EnergyCurve) -> Tuple[float, dict[str, float]]:
        """Get overall composition score (0-100)"""
        progression_score = GratificationScorer.score_energy_progression(energy_curve)
        peak_score = GratificationScorer.score_peak_placement(energy_curve)
        variety_score = GratificationScorer.score_variety_vs_repetition(energy_curve)

        overall = progression_score * 0.4 + peak_score * 0.4 + variety_score * 0.2

        return overall, {
            "progression": progression_score,
            "peak_placement": peak_score,
            "variety": variety_score,
            "overall": overall
        }
