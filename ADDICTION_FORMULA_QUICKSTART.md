# Addiction Formula Quick Start Guide

## What You Now Have

Your Beat Addicts system now generates music using **The Addiction Formula** — scientifically-proven songwriting principles that create psychological engagement and replay value.

## Key Principles (30 Second Version)

- **Energy Curves**: Songs should gradually build energy overall
- **Gratification + Anticipation**: Choruses reward, verses build desire
- **Hollywood Structure**: 3-peak pattern (biggest moment at end)
- **1-2-3 Rule**: Introduce → Repeat → Change (prevents boredom)

## How to Use

### Option 1: Simple Usage (Backward Compatible)

```python
from beat_addicts import SongBuilder

builder = SongBuilder()
result = builder.build_song(
    "An epic story about pursuing dreams",
    duration=15
)
# Now automatically uses Addiction Formula principles
```

### Option 2: Advanced Usage (Full Control)

```python
from beat_addicts import AddictionFormulaSongBuilder

builder = AddictionFormulaSongBuilder()
result = builder.build_song_with_addiction_formula(
    prompt="An epic story about pursuing dreams",
    genre="pop",  # or "house", "lofi", "ambient", etc.
    duration=15,
    enable_composition_scoring=True  # Get quality score
)

print(f"Composition Score: {result['composition_score']}/100")
# Returns: 0-100 score showing adherence to principles
```

### What You Get Back

```python
{
    "song_id": "song_1234567890",
    "title": "Your Song Title",
    "lyrics_path": "output/song_xxx/lyrics.txt",
    "song_path": "output/song_xxx/song.mp3",
    "analysis_path": "output/song_xxx/composition.json",
    "composition_score": 85.5,  # 0-100
    "genre": "pop",
    "duration": 15,
    "energy_curve": [10, 25, 35, 60, 40, ...]  # 12 energy points
}
```

## Understanding the Composition Score

**0-100 scale** measuring how well your song follows proven engagement principles:

- **80-100**: Excellent - follows principles precisely
- **60-79**: Good - solid structure, minor improvements possible
- **40-59**: Fair - needs adjustment to energy curve
- **0-39**: Poor - needs major restructuring

Score evaluates:

- Does energy build overall? (progression)
- Is biggest moment at the end? (peak placement)
- Does it follow 1-2-3 rule? (variety)

## Supported Genres

Each has optimized arrangement guidance:

```python
builder.build_song_with_addiction_formula(
    prompt="...",
    genre="pop"          # Pop with hooks & layers
)

# Also try: "house", "lofi", "ambient", "drum_and_bass"
```

## Song Structure You Get

All generated songs follow this proven structure:

1. **Intro** (10% energy) - Establish mood
2. **Verse 1** (30%) - Build anticipation
3. **Pre-Chorus** (40%) - Maximum tension
4. **Chorus 1** (60%) - First reward
5. **Verse 2** (40%) - Deeper development
6. **Pre-Chorus 2** (45%) - Build again
7. **Chorus 2** (75%) - Bigger reward
8. **Bridge** (50-80%) - New territory + max tension
9. **Chorus 3** (95%) - THE CLIMAX
10. **Chorus 4** (100%) - Euphoria
11. **Outro** (15%) - Return to intro

## Run Examples

See the system in action:

```bash
# All examples
python examples_addiction_formula.py

# Individual examples
python examples_addiction_formula.py 1  # Basic generation
python examples_addiction_formula.py 3  # Composition analysis
python examples_addiction_formula.py 4  # See guidance for each section
python examples_addiction_formula.py 5  # Compare different strategies
```

## Under the Hood: What Happens

1. **Energy Curve Generation**
   - Creates 12-point energy trajectory following Hollywood 3-act structure
   - Ensures peaks increase over time

2. **Composition Guide Creation**
   - Maps each section to energy targets
   - Provides arrangement guidance per section

3. **Prompt Enhancement**
   - Enriches your prompt with section-specific instructions
   - Adds genre-specific details

4. **Music Generation**
   - AudioCraft MusicGen creates track following enhanced prompt

5. **Composition Scoring**
   - Evaluates adherence to principles (optional)
   - Returns 0-100 quality score

## Practical Tips

### For Maximum Engagement

✓ Trust the structure - it's proven in 100+ years of storytelling
✓ Let each section build on the last
✓ Make Verse 2 bigger than Verse 1
✓ Let Bridge be completely different
✓ Make Chorus 3 the emotional climax
✓ Keep Outro short and personal

### Common Mistakes (Now Prevented)

✗ Flat energy throughout song
✗ Biggest moment in the middle
✗ Repeating Verse 1 identically as Verse 2
✗ Chorus that's too big too soon
✗ Bridge that doesn't feel surprising
✗ Outro that doesn't feel like closure

## Integration with Your Workflow

Works seamlessly with existing Beat Addicts features:

```python
from beat_addicts import AddictionFormulaSongBuilder

# Your existing setup
builder = AddictionFormulaSongBuilder(output_dir="my_music")

# Generate multiple songs
for mood in ["uplifting", "introspective", "energetic"]:
    result = builder.build_song_with_addiction_formula(
        prompt=f"A {mood} dance track",
        genre="house",
        duration=15
    )
    print(f"{mood}: {result['composition_score']}/100")
```

## Files Added

- `beat_addicts/addiction_formula.py` - Core implementation
- `beat_addicts/song_builder_addiction.py` - Enhanced builder
- `ADDICTION_FORMULA_GUIDE.py` - Reference documentation
- `examples_addiction_formula.py` - Working examples
- `ADDICTION_FORMULA_QUICKSTART.md` - This file

## Learn More

See `ADDICTION_FORMULA_GUIDE.py` for:

- Detailed section-by-section guidance
- 9 transition types explained
- Quality checklist
- Genre-specific templates

## Quick Reference: The Formula

```
What Makes Songs Addictive?

1. GRATIFICATION (choruses)
   - Reward listeners for paying attention
   - Make each bigger than the last
   
2. ANTICIPATION (verses)  
   - Build desire with tension
   - Create need for gratification
   
3. PACING
   - Big moment every 8-10 bars
   - Otherwise listener zones out
   
4. STRUCTURE
   - 3 energy peaks (intro-setup-peak, build, climax)
   - Peaks spaced throughout song
   - Biggest at very end
   
5. TRANSITIONS
   - Smooth builds to peaks
   - Surprising drops back to verses
   - Prevents predictability
```

## That's It

Start generating music with proven psychological principles:

```python
from beat_addicts import AddictionFormulaSongBuilder

builder = AddictionFormulaSongBuilder()
song = builder.build_song_with_addiction_formula(
    "Your creative idea here",
    genre="pop",
    duration=15
)

print(f"Quality Score: {song['composition_score']}/100")
```

Happy composing! 🎵
