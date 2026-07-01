"""
Addiction Formula Guide for Beat Addicts

Quick reference for using scientifically-proven songwriting principles
with your music generation system.
"""

# CORE CONCEPTS FROM THE ADDICTION FORMULA
# ==========================================

CORE_CONCEPTS = """
1. ENERGY CURVES
   - Hype: Abrupt changes in energy (adds/removes instruments)
   - Tension: Gradual buildup of energy (opens filters, adds layers)
   - Together: Control how engaged listeners stay

2. GRATIFICATION & ANTICIPATION
   - Gratification: Peak moments (choruses) that reward the listener
   - Anticipation: Building sections (verses) that create desire
   - Balance: Switch at right moments or listener disengages

3. HOLLYWOOD 3-ACT STRUCTURE (Most Effective)
   - Act 1 (Setup): Intro + Verse 1 + Pre-Chorus + Chorus 1
     → Establishes mood, introduces problem
   - Act 2 (Confrontation): Verse 2 + Pre-Chorus 2 + Chorus 2 + Bridge
     → Develops problem, increases stakes
   - Act 3 (Resolution): Chorus 3 + Chorus 4 + Outro
     → Climax and payoff

4. THE 1-2-3 RULE
   - 1: Introduce (new section)
   - 2: Repeat (establish pattern)
   - 3: Change (surprise, vary)
   Prevents boredom while maintaining coherence
"""

# SECTION-BY-SECTION GUIDANCE
# ============================

SECTION_GUIDANCE = {
    "INTRO": {
        "purpose": "Set status quo, establish sound",
        "energy": "LOWEST in entire song",
        "hype": "10-20%",
        "tension": "0%",
        "arrangement": "Minimal, atmospheric",
        "tip": "Make sounds interesting - listener decides to stay based on this"
    },
    
    "VERSE_1": {
        "purpose": "Introduce problem, foreshadow chorus",
        "energy": "LOW-MID, building",
        "hype": "20-35%",
        "tension": "20-40%",
        "arrangement": "Sparse, intimate",
        "tip": "Don't stay flat - gradually increase hype every 4-8 bars"
    },
    
    "PRE_CHORUS": {
        "purpose": "Create tension, act as pivot to chorus",
        "energy": "BUILDING",
        "hype": "30-45%",
        "tension": "40-60%",
        "arrangement": "Add percussion opens, filter sweeps",
        "tip": "This is where all tension-building happens. Make it undeniable"
    },
    
    "CHORUS_1": {
        "purpose": "First gratification peak - establish scope",
        "energy": "HIGH (but not maximum)",
        "hype": "60-70%",
        "tension": "20-40%",
        "arrangement": "Full but not bloated",
        "tip": "Write final chorus first, then STRIP elements for chorus 1"
    },
    
    "VERSE_2": {
        "purpose": "Character development - MUST be bigger than Verse 1",
        "energy": "MID-HIGH, more than Verse 1",
        "hype": "35-50%",
        "tension": "50-70%",
        "arrangement": "Richer than Verse 1, add implied tension",
        "tip": "BIGGEST MISTAKE: repeating Verse 1. Add elements, variation"
    },
    
    "PRE_CHORUS_2": {
        "purpose": "Build to bigger chorus",
        "energy": "MORE intense than first",
        "hype": "40-50%",
        "tension": "60-75%",
        "arrangement": "More layers than first pre-chorus",
        "tip": "This should feel like more buildup, more inevitable"
    },
    
    "CHORUS_2": {
        "purpose": "Second gratification - bigger than Chorus 1",
        "energy": "HIGH (bigger)",
        "hype": "75-85%",
        "tension": "30-50%",
        "arrangement": "Unmute 1-2 new tracks from Chorus 1",
        "tip": "Subtle addition - maybe backing vocals or new synth layer"
    },
    
    "PRIMARY_BRIDGE": {
        "purpose": "Maximum tension before finale",
        "energy": "VARIABLE - explore new territory",
        "hype": "30-60% (unexpected shift)",
        "tension": "70-90% (highest in song)",
        "arrangement": "Completely new sounds, key change, rap section, anything",
        "tip": "If Song feels predictable, save it with a creative bridge"
    },
    
    "CHORUS_3": {
        "purpose": "THE CLIMAX - biggest moment in entire song",
        "energy": "MAXIMUM",
        "hype": "95-100%",
        "tension": "40-60%",
        "arrangement": "All instruments, full stereo, maximum density",
        "tip": "Every previous section builds to THIS moment"
    },
    
    "CHORUS_4": {
        "purpose": "Finale - celebrate, extend, don't retreat",
        "energy": "SUSTAINED HIGH",
        "hype": "100%",
        "tension": "50-70%",
        "arrangement": "Add solos, ad-libs, guitar leads, strings",
        "tip": "People who disliked song already left - go crazy"
    },
    
    "OUTRO": {
        "purpose": "Return to status quo - personal, reflective",
        "energy": "LOW (echo of intro)",
        "hype": "10-25%",
        "tension": "5-10%",
        "arrangement": "Sparse, similar to intro",
        "tip": "Keep SHORT. Leave them wanting. Ends on groove or cold"
    }
}

# 9 TRANSITION TYPES
# ==================

TRANSITIONS = {
    "JUMP": {
        "description": "Abrupt hype change",
        "how": "Suddenly add/remove instruments every 4-8 bars",
        "best_for": "Verse to verse, pre-chorus to chorus",
        "strength": "POWERFUL - clear, in-your-face",
        "risk": "Can sound chaotic if overused"
    },
    
    "SMOOTH": {
        "description": "Gradual hype increase + tension",
        "how": "Layer instruments progressively, open filters slowly",
        "best_for": "Build-ups, verse to chorus",
        "strength": "Most popular, great direction",
        "risk": "Predictable if template-y"
    },
    
    "DROP": {
        "description": "Sudden energy decrease",
        "how": "Strip out instruments, cut percussion",
        "best_for": "Chorus to verse return",
        "strength": "Surprising, keeps attention",
        "risk": "Listeners may turn off - follow with tension to re-engage"
    },
    
    "SURPRISE": {
        "description": "Build tension then drop hype",
        "how": "Add rising tension, then suddenly lower energy",
        "best_for": "High-emotion moments before verse",
        "strength": "Very emotional, gripping",
        "risk": "Can feel disappointing if not handled well"
    },
    
    "LIFT": {
        "description": "Less tension than expected for hype increase",
        "how": "Jump up in hype without much lead-in",
        "best_for": "Explosive chorus entries",
        "strength": "Punchy, powerful, establishes new section",
        "risk": "Can feel abrupt if timing is off"
    },
    
    "NEGATIVE_TENSION": {
        "description": "Gradual decrease to lower hype",
        "how": "Remove instruments slowly, lower pitches gradually",
        "best_for": "Descending energy, outros",
        "strength": "Smooth, beautiful wind-down",
        "risk": "Rarely used - be intentional"
    },
    
    "FLATLINE": {
        "description": "No change in hype level",
        "how": "Keep instruments the same, vary within section",
        "best_for": "Only if you have killer hook/rhythm",
        "strength": "Can work if melody/groove is exceptional",
        "risk": "BORING if not done with purpose - usually avoid"
    },
    
    "OVERSHOOT": {
        "description": "Build more tension than needed",
        "how": "Over-prepare, more buildup than payoff",
        "best_for": "Rarely - creates anticlimactic feeling",
        "strength": "Implies underlying turmoil",
        "risk": "DON'T USE - wastes listener's anticipation"
    },
    
    "FALSE_PROMISE": {
        "description": "Build tension but stay at same hype",
        "how": "Add tension but don't increase hype",
        "best_for": "Risky moment for drama",
        "strength": "Unexpected emotional beat",
        "risk": "DANGEROUS - may anger listener if overused"
    }
}

# QUICK CHECKLIST FOR YOUR SONG
# =============================

QUALITY_CHECKLIST = """
✓ GLOBAL ENERGY PROGRESSION
  - Is the ending bigger than the beginning?
  - Do later sections generally exceed earlier ones?

✓ PEAK PLACEMENT
  - Is Chorus 3 the biggest moment?
  - Is it in the last 1/3 of the song?

✓ THE 1-2-3 RULE
  - Do sections follow: Introduce → Repeat → Change pattern?
  - Do I ever repeat a section identically? (FIX THIS)

✓ VERSE QUALITY
  - Is Verse 2 bigger than Verse 1?
  - Did I add elements, not just repeat?

✓ TRANSITIONS
  - Do builds lead somewhere?
  - Or do they end in false promises?

✓ TENSION BUILDUP
  - Can listener feel anticipation building?
  - Pre-choruses are maximum tension spots?

✓ GRATIFICATION PAYOFF
  - Do choruses feel like earned rewards?
  - Is each chorus bigger than the last?

✓ BRIDGE IMPACT
  - Does bridge feel like "new territory"?
  - Is it different enough from verses/chorus?

✓ PACING
  - Is there a big moment every 8-10 seconds?
  - Would listener stay engaged or zone out?

✓ LISTENER EXPERIENCE
  - Could someone draw your energy curve just by listening?
  - Do they feel addicted to replay, or bored after one listen?
"""

# PRACTICAL PROMPT TEMPLATES FOR YOUR GENERATOR
# ==============================================

COMPOSITION_TEMPLATES = {
    "POP_UPLIFTING": """
Create an uplifting pop song with:
- Intro: Minimal, establish mood
- Verse 1: Introspective, building curiosity  
- Chorus 1: Bright, approachable (don't go full energy yet)
- Verse 2: More elements than V1, moving story forward
- Chorus 2: Bigger than first chorus
- Bridge: Unexpected twist, emotional peak, new sound
- Chorus 3: THE BIG MOMENT - euphoric, all elements
- Outro: Reflective callback to intro
""",
    
    "HOUSE_DANCEFLOOR": """
Create a house track with:
- Intro: Minimal kick + minimal percussion (8 bars)
- Verse 1: Add deep bass, synth pads, 4/4 locked
- Pre-Chorus: Tension rise, add filtered strings
- Chorus 1: Kick + bass locked, backing vocals
- Verse 2: More hi-hat openings, builds anticipation
- Pre-Chorus 2: More dramatic bass drop
- Chorus 2: Add arps, more vocal layers
- Bridge: 8-16 bar tension buildup or breakdown
- Chorus 3: Full energy return, dramatic entrance
- Outro: Fade out or cold stop after final chorus
""",

    "LOFI_CHILL": """
Create a lo-fi track with:
- Intro: Warm, vintage, minimal (vinyl warmth)
- Verse 1: Add jazzy chords, soft drums, swing feel
- Chorus 1: Add bass line, more melodic elements
- Verse 2: Richer harmony than V1, more instruments
- Chorus 2: Subtle strings or pad layering
- Bridge: Stripped down moment or different key center
- Final Chorus: Full arrangement, all elements
- Outro: Fade with vinyl crackle or sudden cold end
""",
}

# HOW TO USE WITH BEAT_ADDICTS
# ============================

USAGE_EXAMPLE = """
# Using Addiction Formula with your Beat Addicts

from beat_addicts.song_builder_addiction import AddictionFormulaSongBuilder

# Create builder
builder = AddictionFormulaSongBuilder(output_dir="output")

# Generate song with composition analysis
result = builder.build_song_with_addiction_formula(
    prompt="An uplifting story about overcoming self-doubt",
    genre="pop",
    duration=15,
    enable_composition_scoring=True
)

# Result includes:
# - Lyrics written with section structure
# - Energy curve analysis
# - Composition score (0-100) showing adherence to formula
# - Section-by-section breakdown
# - Composition details saved to JSON

print(f"Composition Score: {result['composition_score']}/100")
print(f"Energy Curve: {result['energy_curve']}")

# Access detailed analysis
import json
with open(result['analysis_path']) as f:
    analysis = json.load(f)
    print(f"Energy progression: {analysis['score_details']}")
"""

if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*50 + "\n")
    print("SECTION-BY-SECTION GUIDANCE:")
    for section, guidance in SECTION_GUIDANCE.items():
        print(f"\n{section}:")
        for key, val in guidance.items():
            print(f"  {key}: {val}")
