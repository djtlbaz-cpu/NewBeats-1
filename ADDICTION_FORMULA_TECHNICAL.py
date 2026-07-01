"""
ADDICTION FORMULA - TECHNICAL IMPLEMENTATION GUIDE

For developers who want to understand, extend, or integrate the system.
"""

# ============================================================================
# ARCHITECTURE OVERVIEW
# ============================================================================

ARCHITECTURE_OVERVIEW = """
The Addiction Formula implementation follows a layered architecture:

┌─────────────────────────────────────────────────────────────┐
│  Application Layer: AddictionFormulaSongBuilder              │
│  - High-level interface for music generation                │
│  - Manages full workflow (lyrics → sections → music)        │
│  - Provides progress tracking and composition scoring       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│  Composition Layer: CompositionGuide, EnergyCurve            │
│  - Section-by-section arrangement guidance                  │
│  - Energy curve generation and management                   │
│  - Transition type mapping                                  │
│  - Genre-specific enhancement                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│  Scoring Layer: GratificationScorer                          │
│  - Evaluates composition quality                            │
│  - Calculates adherence metrics                             │
│  - Provides feedback for refinement                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│  Model Layer: MusicGen (AudioCraft)                         │
│  - Generates audio from prompts                             │
│  - Handles device management                                │
│  - Audio writing and format conversion                      │
└─────────────────────────────────────────────────────────────┘


# ============================================================================
# KEY CLASSES AND THEIR RESPONSIBILITIES
# ============================================================================

EnergyCurve (addiction_formula.py)
├─ Responsibility: Model energy progression through song
├─ Key Methods:
│  ├─ __init__(num_peaks=3): Initialize with 3-peak Hollywood structure
│  ├─ get_energy_at_point(index): Get energy value at specific point
│  ├─ get_total_energy_curve(): Get all energy values
│  └─ is_globally_increasing(): Check if overall energy builds
├─ Key Properties:
│  ├─ num_peaks: Number of energy peaks (typically 3)
│  └─ points: List of EnergyPoint objects (12 for Hollywood)
└─ Extension Ideas:
   ├─ Different curve types (2-peak, 4-peak, experimental)
   ├─ Dynamic curve adjustment based on feedback
   └─ Album-level energy sequencing


CompositionGuide (addiction_formula.py)
├─ Responsibility: Provide arrangement & production guidance per section
├─ Key Methods:
│  ├─ __init__(genre, energy_curve): Initialize with genre and curve
│  ├─ get_section_prompt_modifiers(section): Get section-specific tweaks
│  ├─ get_transition_guidance(transition): Explain transition type
│  ├─ generate_arrangement_prompt(section): Create prompt for section
│  └─ generate_full_composition_prompt(genre_prompt): Full guidance
├─ Key Properties:
│  ├─ genre: Music genre ("pop", "house", "lofi", etc.)
│  ├─ sections: List of SectionConfig objects (14 total)
│  └─ energy_curve: Reference to EnergyCurve
└─ Extension Ideas:
   ├─ Add more genres with specific patterns
   ├─ Custom section configurations
   ├─ Dynamic modifier generation based on analysis
   └─ Linked section recommendations


GratificationScorer (addiction_formula.py)
├─ Responsibility: Score composition quality (0-100)
├─ Static Methods:
│  ├─ score_energy_progression(): How much does energy build?
│  ├─ score_peak_placement(): Is biggest moment at end?
│  ├─ score_variety_vs_repetition(): 1-2-3 rule adherence?
│  └─ score_composition(): Overall score with breakdown
├─ Scoring Metrics:
│  ├─ Progression: 0-100 based on second-half > first-half energy
│  ├─ Peak: 0-100 based on max energy location (100 if in last 60%)
│  └─ Variety: 0-100 based on energy point differences
└─ Extension Ideas:
   ├─ Add hook/groove scoring (once integrated with generation)
   ├─ Listener model prediction (estimated replay rate)
   ├─ Genre-specific scoring adjustments
   └─ Historical comparison against generated songs


AddictionFormulaSongBuilder (song_builder_addiction.py)
├─ Responsibility: Orchestrate full music generation workflow
├─ Key Methods:
│  ├─ build_song_with_addiction_formula(): Main entry point
│  ├─ _generate_lyrics_with_structure(): Create structured lyrics
│  ├─ _generate_music_sections(): Map sections to timing
│  ├─ _build_enhanced_music_prompt(): Create rich music prompt
│  └─ _get_genre_specifics(): Genre enhancement details
├─ Key Properties:
│  ├─ output_dir: Where to save generated songs
│  ├─ lyrics_gen: LyricsGenerator instance
│  └─ melody_gen: MelodyGenerator instance
└─ Extension Ideas:
   ├─ Save intermediate section generations separately
   ├─ Batch generation with scoring
   ├─ Iterative refinement loop
   └─ Album generation workflow


# ============================================================================
# DATA STRUCTURES
# ============================================================================

EnergyPoint (dataclass)
├─ Fields:
│  ├─ hype: float (0-100) - Abrupt changes
│  └─ tension: float (0-100) - Gradual buildup
└─ Properties:
   └─ total_energy: (hype * 0.6) + (tension * 0.4)


SectionConfig (dataclass)
├─ Fields:
│  ├─ section: SongSection enum value
│  ├─ energy_start: EnergyPoint
│  ├─ energy_end: EnergyPoint
│  ├─ transition_type: TransitionType enum
│  ├─ bars: int (8-bar sections count)
│  └─ description: str (section purpose/guidance)
└─ Purpose: Defines energy targets and guidance per section


# ============================================================================
# ENUMERATION TYPES
# ============================================================================

SongSection Enum (14 Values)
├─ INTRO: Establish mood, lowest energy
├─ VERSE_1: Introduce problem
├─ VERSE_CONT: (Optional extension)
├─ PRE_CHORUS: Build tension
├─ CHORUS_1: First reward (medium)
├─ VERSE_2: Character development
├─ PRE_CHORUS_2: Build again
├─ CHORUS_2: Bigger reward
├─ PRIMARY_BRIDGE: New territory
├─ BRIDGE_CONT: Continue bridge
├─ CHORUS_3: THE CLIMAX
├─ CHORUS_4: Finale
└─ OUTRO: Return to status quo


TransitionType Enum (9 Values)
├─ JUMP: Abrupt hype change every 4-8 bars
├─ SMOOTH: Gradual hype + tension increase
├─ DROP: Sudden energy decrease
├─ SURPRISE: Build tension then drop hype
├─ OVERSHOOT: Over-build (use sparingly)
├─ FALSE_PROMISE: Build tension, same hype
├─ FLATLINE: No change (risky)
├─ LIFT: Less tension than expected for hype
└─ NEGATIVE_TENSION: Gradual energy decrease


# ============================================================================
# WORKFLOW: STEP-BY-STEP EXECUTION
# ============================================================================

1. INITIALIZATION
   ├─ AddictionFormulaSongBuilder created
   ├─ MelodyGenerator & LyricsGenerator initialized
   └─ Output directory prepared

2. ENERGY CURVE GENERATION
   ├─ EnergyCurve created (defaults to 3-peak Hollywood)
   ├─ 12 EnergyPoints generated
   └─ Energy values set per formula

3. COMPOSITION GUIDE CREATION
   ├─ CompositionGuide initialized with genre
   ├─ 14 SectionConfig objects created
   ├─ Energy targets assigned per section
   └─ Transition types mapped

4. LYRICS GENERATION
   ├─ Structure guidance created
   ├─ LyricsGenerator.generate() called with structure prompt
   ├─ Lyrics saved to file
   └─ Progress tracked (typically 40% of total)

5. MUSIC SECTIONS MAPPING
   ├─ 14 sections mapped to song timing
   ├─ Energy targets calculated per section
   ├─ Section prompts generated
   └─ Metadata saved

6. ENHANCED MUSIC PROMPT GENERATION
   ├─ Base composition prompt created from CompositionGuide
   ├─ Genre specifics added
   ├─ Full structure guidance included
   └─ Rich prompt ready for generation

7. MUSIC GENERATION
   ├─ MusicGen.generate() called with enhanced prompt
   ├─ Audio generated (progress tracked at 45-90%)
   ├─ Audio saved to MP3
   └─ Duration maintained

8. COMPOSITION SCORING (Optional)
   ├─ GratificationScorer evaluates energy curve
   ├─ Three metrics calculated:
   │  ├─ Energy progression (0-100)
   │  ├─ Peak placement (0-100)
   │  └─ Variety score (0-100)
   ├─ Overall score computed (weighted average)
   └─ Results included in output

9. ANALYSIS SAVING
   ├─ Energy curve values saved
   ├─ Composition scores saved
   ├─ Section metadata saved
   ├─ Original prompt saved
   └─ All saved to JSON for reference

10. RETURN RESULTS
    ├─ Song ID, title, paths returned
    ├─ Composition score included
    ├─ Genre, duration included
    └─ Full energy curve included


# ============================================================================
# EXTENSION POINTS
# ============================================================================

1. ADD NEW GENRES
   Location: AddictionFormulaSongBuilder._get_genre_specifics()
   
   Example:
   ├─ Add new genre key to genre_specs dict
   ├─ Define specific arrangement guidance
   ├─ Include typical structure for that genre
   └─ CompositionGuide will auto-apply


2. CUSTOMIZE ENERGY CURVES
   Location: EnergyCurve.__init__() and _generate_hollywood_curve()
   
   Example:
   ├─ Add num_peaks parameter handling (2, 4, 5, etc.)
   ├─ Create alternative curve generators
   ├─ Support experimental structures
   └─ Override specific energy points


3. ADD SCORING METRICS
   Location: GratificationScorer (add new static methods)
   
   Ideas:
   ├─ score_groove_consistency()
   ├─ score_genre_adherence()
   ├─ score_emotional_arc()
   ├─ predict_replay_rate()
   └─ Call in score_composition()


4. ITERATIVE REFINEMENT LOOP
   Extension to AddictionFormulaSongBuilder:
   
   ├─ Generate initial song
   ├─ Score composition
   ├─ If score < threshold:
   │  ├─ Adjust energy curve
   │  ├─ Regenerate with new guidance
   │  └─ Repeat
   └─ Return best scored result


5. BATCH GENERATION WITH ANALYSIS
   Extension to AddictionFormulaSongBuilder:
   
   ├─ Generate multiple songs in parallel
   ├─ Compare composition scores
   ├─ Generate album-level energy arc
   ├─ Export comparative analysis
   └─ Select best performing songs


6. ALBUM/EP WORKFLOW
   New class: AlbumBuilder
   
   ├─ Create multi-song energy arc
   ├─ Generate cohesive concept
   ├─ Maintain thematic consistency
   ├─ Export album metadata
   └─ Generate visual representations


# ============================================================================
# PERFORMANCE CONSIDERATIONS
# ============================================================================

Memory:
├─ EnergyCurve: ~1KB (12 EnergyPoints)
├─ CompositionGuide: ~5KB (14 SectionConfigs)
├─ Full generation: ~100MB+ (audio samples)
└─ Optimize: Lazy load generation, stream audio

Processing:
├─ Energy curve generation: <1ms
├─ Composition scoring: <10ms
├─ Music generation: 30-60 seconds (model dependent)
├─ Lyric generation: 10-20 seconds
└─ Total: ~1-2 minutes per song

Bottleneck:
├─ MusicGen inference (30-90% of time)
├─ Solution: Use smaller model for drafts, larger for final


# ============================================================================
# TESTING RECOMMENDATIONS
# ============================================================================

Unit Tests:
├─ EnergyPoint.total_energy calculations
├─ EnergyCurve.is_globally_increasing() logic
├─ SectionConfig constraint validation
├─ GratificationScorer metric calculations
└─ Prompt generation determinism

Integration Tests:
├─ Full composition generation workflow
├─ Section mapping to timing
├─ Lyrics + music coordination
├─ File I/O and JSON serialization
└─ Progress callback firing

Regression Tests:
├─ Verify composition scores stable
├─ Check energy curves remain valid
├─ Validate section guidance consistency
└─ Compare scores against reference songs


# ============================================================================
# DEBUGGING TIPS
# ============================================================================

Enable verbose output:
├─ Add print() statements in workflow methods
├─ Check progress_callback is firing correctly
├─ Verify energy_curve.points are in expected range
└─ Save intermediate prompts to inspect

Check composition quality:
├─ Print energy_curve.get_total_energy_curve()
├─ Run GratificationScorer.score_composition()
├─ Inspect score_details breakdown
├─ Compare against reference curves

Verify prompt quality:
├─ Print generated_prompt before MusicGen
├─ Check for genre-specific modifiers
├─ Validate section guidance is present
└─ Compare with manual prompts


# ============================================================================
# FUTURE ENHANCEMENTS
# ============================================================================

Near-term:
├─ Visualization of energy curves
├─ Comparative analysis UI
├─ Genre detection from generated music
└─ User feedback loop

Medium-term:
├─ Real-time generation feedback
├─ Multi-artist collaboration workflow
├─ Style transfer between songs
└─ Ablation testing (remove sections)

Long-term:
├─ End-to-end training on successful songs
├─ Listener model prediction
├─ Generative adversarial framework
├─ Full album generation with cohesion
└─ Real-time generation with A/B testing


# ============================================================================
# REFERENCES
# ============================================================================

"The Addiction Formula" - Friedemann Findeisen (2015)
├─ Core psychological principles
├─ Energy curve modeling
├─ Transition types
└─ Section guidance

Hollywood Screenplay Structure - Syd Field
├─ 3-act structure
├─ Pacing principles
└─ Character arc concepts

Music Psychology
├─ Gratification-anticipation cycles
├─ Listener engagement metrics
├─ Emotional response patterns
└─ Replay value factors
"""

# Quick Reference: Key Formulas
# =============================

# Total Energy = (Hype * 0.6) + (Tension * 0.4)
#   → 60% weight on abrupt changes, 40% on gradual buildup

# Progression Score = (Second Half Avg - First Half Avg) / 100 * 100
#   → Measure of overall energy build

# Peak Placement Score:
#   - 100 if max in last 60%
#   - 50 if in last 40%
#   - 10 otherwise

# Variety Score:
#   - 100 if average energy diff 10-30
#   - 75 if 5-40
#   - 40 otherwise

# Overall Score = (Progression * 0.4) + (Peak * 0.4) + (Variety * 0.2)
#   → Weighted average of three metrics
