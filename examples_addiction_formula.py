#!/usr/bin/env python3
"""
Example: Using Addiction Formula with Beat Addicts

Demonstrates how to generate music using scientifically-proven
songwriting principles for maximum listener engagement.
"""

import sys
from beat_addicts import AddictionFormulaSongBuilder


def example_basic_generation():
    """Generate a single song with Addiction Formula"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Song Generation with Addiction Formula")
    print("=" * 60)
    
    builder = AddictionFormulaSongBuilder(output_dir="output")
    
    prompt = "A triumphant song about overcoming adversity"
    
    def progress(val: float) -> None:
        print(f"Progress: {val}%")
    
    result = builder.build_song_with_addiction_formula(
        prompt=prompt,
        genre="pop",
        duration=15,
        progress_callback=progress,
        enable_composition_scoring=True
    )
    
    print(f"\n✓ Generated: {result['title']}")
    print(f"✓ Score: {result['composition_score']:.1f}/100")
    print(f"✓ Files saved to: {result['song_id']}/")
    print(f"  - Lyrics: {result['lyrics_path']}")
    print(f"  - Music: {result['song_path']}")
    print(f"  - Analysis: {result['analysis_path']}")
    print(f"\nEnergy curve: {[f'{e:.0f}%' for e in result['energy_curve']]}")
    
    return result


def example_genre_specific():
    """Generate songs in different genres"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Genre-Specific Composition")
    print("=" * 60)
    
    builder = AddictionFormulaSongBuilder(output_dir="output")
    
    prompts = {
        "lofi": "A relaxing study session with cozy vibes",
        "house": "An energetic dancefloor anthem about freedom",
        "ambient": "A meditative journey through space and time",
    }
    
    for genre, prompt in prompts.items():
        print(f"\nGenerating {genre.upper()}...")
        result = builder.build_song_with_addiction_formula(
            prompt=prompt,
            genre=genre,
            duration=12,
            enable_composition_scoring=True
        )
        print(f"  Score: {result['composition_score']:.1f}/100 - {result['title']}")


def example_composition_analysis():
    """Show detailed composition analysis"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Detailed Composition Analysis")
    print("=" * 60)
    

    from beat_addicts import EnergyCurve, GratificationScorer
    
    # Create energy curve
    curve = EnergyCurve(num_peaks=3)
    
    # Score it
    score, details = GratificationScorer.score_composition(curve)
    
    print(f"\nComposition Score: {score:.1f}/100")
    print("\nBreakdown:")
    print(f"  - Energy Progression: {details['progression']:.1f}/100")
    print("    (Does song build overall? Last sections bigger than first?)")
    print(f"\n  - Peak Placement: {details['peak_placement']:.1f}/100")
    print("    (Is biggest moment at the end?)")
    print(f"\n  - Variety vs Repetition: {details['variety']:.1f}/100")
    print("    (Does it follow 1-2-3 rule? Balanced change?)")
    
    energies = curve.get_total_energy_curve()
    print("\nEnergy points through song:")
    sections = [
        "Intro", "V1", "PreC", "C1", "V2", "PreC2", "C2", "Bridge", "C3", "C4", "Outro", "Buffer"
    ]
    for _, (section, energy) in enumerate(zip(sections, energies)):
        bar = "█" * int(energy / 10) + "░" * (10 - int(energy / 10))
        print(f"  {section:6} {bar} {energy:.0f}%")


def example_manual_composition_guide():
    """Show how to use composition guide for manual writing"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Using Composition Guide (Manual Reference)")
    print("=" * 60)
    
    from beat_addicts import CompositionGuide, ElementGuidance, SongSection, TensionType
    
    _guide = CompositionGuide(genre="pop")
    
    # Get guidance for a few sections
    sections_to_check = [
        SongSection.INTRO,
        SongSection.VERSE_1,
        SongSection.PRE_CHORUS,
        SongSection.CHORUS_1,
        SongSection.PRIMARY_BRIDGE,
        SongSection.CHORUS_3,
    ]
    
    for section in sections_to_check:
        # Note: get_arrangement_guidance is a static method that doesn't require section info
        guidance = ElementGuidance.get_arrangement_guidance(TensionType.REGULAR)
        print(f"\n{section.value.upper()}:")
        print(str(guidance)[:200] + "...")


def example_scoring_different_curves():
    """Compare different energy curve strategies"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Comparing Different Energy Strategies")
    print("=" * 60)
    
    from beat_addicts import EnergyCurve, GratificationScorer, EnergyPoint
    
    # Standard Hollywood curve
    standard_curve = EnergyCurve(num_peaks=3)
    standard_score, _ = GratificationScorer.score_composition(standard_curve)
    
    # Manual curve: Energy stays flat
    flat_curve = EnergyCurve(num_peaks=3)
    flat_curve.points = [EnergyPoint(hype=50, tension=50) for _ in range(12)]
    flat_score, _ = GratificationScorer.score_composition(flat_curve)
    
    # Manual curve: Builds to peak in middle (wrong)
    peak_middle = EnergyCurve(num_peaks=3)
    peak_middle.points = [
        EnergyPoint(10, 0), EnergyPoint(30, 10), EnergyPoint(50, 20),
        EnergyPoint(100, 80), EnergyPoint(90, 60),  # Peak too early!
        EnergyPoint(80, 50), EnergyPoint(70, 40), EnergyPoint(60, 30),
        EnergyPoint(50, 20), EnergyPoint(40, 10), EnergyPoint(30, 5),
        EnergyPoint(20, 2),
    ]
    middle_peak_score, _ = GratificationScorer.score_composition(peak_middle)
    
    print(f"Standard Hollywood Structure: {standard_score:.1f}/100 ✓")
    print(f"Flat Energy (boring):        {flat_score:.1f}/100 ✗")
    print(f"Peak in Middle (wrong):      {middle_peak_score:.1f}/100 ✗")
    
    print("\nLessons:")
    print("- Standard 3-act structure scores highest")
    print("- Flat energy = bad engagement")
    print("- Peak placement matters! Should be at end")


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  BEAT ADDICTS - ADDICTION FORMULA EXAMPLES                ║")
    print("║  Learn how to generate music using psychological          ║")
    print("║  principles for maximum listener engagement               ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    try:
        # Run examples based on command line arg
        if len(sys.argv) > 1:
            example_num = sys.argv[1]
            if example_num == "1":
                example_basic_generation()
            elif example_num == "2":
                example_genre_specific()
            elif example_num == "3":
                example_composition_analysis()
            elif example_num == "4":
                example_manual_composition_guide()
            elif example_num == "5":
                example_scoring_different_curves()
            else:
                print(f"Unknown example: {example_num}")
                print("Usage: python examples_addiction_formula.py [1-5]")
        else:
            # Run all examples
            example_basic_generation()
            example_composition_analysis()
            example_manual_composition_guide()
            example_scoring_different_curves()
            
            print("\n" + "=" * 60)
            print("All examples completed!")
            print("\nRun individual examples:")
            print("  python examples_addiction_formula.py 1  # Basic generation")
            print("  python examples_addiction_formula.py 2  # Genre-specific")
            print("  python examples_addiction_formula.py 3  # Analysis")
            print("  python examples_addiction_formula.py 4  # Composition guide")
            print("  python examples_addiction_formula.py 5  # Compare strategies")
    
    except (ValueError, IndexError, KeyError) as e:
        print(f"\nError running example: {e}")
        import traceback
        traceback.print_exc()
