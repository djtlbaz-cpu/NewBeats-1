"""
Simple dual bass house generation - standalone without complex imports
"""

import os
import sys
import json
import time
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from beat_addicts.melody_generator import MelodyGenerator


def generate_bass_house_v1():
    """High-energy bass house with explosive drops"""
    print("\n[V1] High-Energy Bass House Generation...")
    
    prompt = (
        "High-energy bass house track inspired by LEVITY Flip It and FISHER. "
        "Start with deep filtered bass synth pad, side-chain compression. "
        "Punchy 808 kicks on downbeats. Layered Hi-Hat rolls every 8 bars. "
        "Surprise drop at 0:30 - sudden silence then massive bass punch. "
        "Wobble bass with LFO automation for tension. "
        "Experimental filtered vocal chops as texture. "
        "Build to climax with accelerating fills. "
        "Electronic/synth instruments only. Club-ready bass focus."
    )
    
    generator = MelodyGenerator()
    print("[V1] Generating audio (45 seconds)...")
    melody = generator.generate(prompt, 45)
    
    # Save
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    song_id = f"v1_higenergy_{int(time.time())}"
    song_dir = os.path.join(output_dir, song_id)
    os.makedirs(song_dir, exist_ok=True)
    
    song_path = os.path.join(song_dir, f"{song_id}.mp3")
    generator.save(melody, song_path[:-4])
    
    print(f"[V1] Saved: {song_path}")
    return {
        "version": 1,
        "title": "High-Energy Bass House with Explosive Drops",
        "song_id": song_id,
        "song_path": song_path,
        "prompt": prompt,
        "duration": 45
    }


def generate_bass_house_v2():
    """Experimental bass house with complex buildups"""
    print("\n[V2] Experimental Bass House Generation...")
    
    prompt = (
        "Experimental bass house with FISHER's unpredictable production. "
        "Open with sparse pad and reverb-heavy filtered bass drone. "
        "Clipped snare breaks at unexpected intervals (non-4/4). "
        "Polyrhythmic percussion - swung 16ths against straight 8ths. "
        "Granular synth textures with random cutoff automation. "
        "Mid-track surprise: tempo shift down 5 BPM, then snap back with filter sweep. "
        "Vocal glitches as rhythmic element (not melody). "
        "Complexity through production layers, not just volume. "
        "Ambiguous semi-resolved ending (creates question mark feeling). "
        "Maximum creative production and experimental texture."
    )
    
    generator = MelodyGenerator()
    print("[V2] Generating audio (50 seconds)...")
    melody = generator.generate(prompt, 50)
    
    # Save
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    song_id = f"v2_experimental_{int(time.time())}"
    song_dir = os.path.join(output_dir, song_id)
    os.makedirs(song_dir, exist_ok=True)
    
    song_path = os.path.join(song_dir, f"{song_id}.mp3")
    generator.save(melody, song_path[:-4])
    
    print(f"[V2] Saved: {song_path}")
    return {
        "version": 2,
        "title": "Experimental Bass House with Complex Buildups",
        "song_id": song_id,
        "song_path": song_path,
        "prompt": prompt,
        "duration": 50
    }


def create_comparison():
    """Create comparison report"""
    
    comparison = {
        "customer_request": "LEVITY - Flip It x FISHER cross - high energy, bass house, experimental, surprise elements",
        "versions_generated": 2,
        "timestamp": int(time.time()),
        "details": {
            "version_1": {
                "focus": "High-energy maximization, explosive drops, club-ready",
                "techniques": [
                    "Surprise drop (silence -> bass punch)",
                    "Wobble bass LFO automation",
                    "Accelerating percussion fills",
                    "808 kicks + hi-hat layering",
                    "Vocal chops as texture",
                    "Side-chain compression"
                ],
                "use_case": "DJ peak time, dance floor, maximum energy"
            },
            "version_2": {
                "focus": "Complexity, listener engagement, production-forward",
                "techniques": [
                    "Polyrhythmic breaks (non-4/4)",
                    "Granular synth automation",
                    "Tempo shift surprise (down 5 BPM)",
                    "Vocal glitches as rhythm",
                    "Unexpected snare breaks",
                    "Ambiguous ending (implied tension)"
                ],
                "use_case": "Underground venue, portfolio showcase, intrigue-focused"
            }
        }
    }
    
    return comparison


def main():
    print("\n" + "="*70)
    print("DUAL BASS HOUSE GENERATION: LEVITY x FISHER")
    print("="*70)
    
    try:
        v1 = generate_bass_house_v1()
        v2 = generate_bass_house_v2()
        
        comparison = create_comparison()
        comparison["v1"] = v1
        comparison["v2"] = v2
        
        # Save report
        report_path = "output/dual_generation_report.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding='utf-8') as f:
            json.dump(comparison, f, indent=2)
        
        print("\n" + "="*70)
        print("SUCCESS: Dual generation complete!")
        print("="*70)
        print(f"\n[REPORT]: {report_path}")
        print("\n[V1 - HIGH-ENERGY]")
        print(f"  Title: {v1['title']}")
        print(f"  Path: {v1['song_path']}")
        print(f"  Duration: {v1['duration']}s")
        
        print("\n[V2 - EXPERIMENTAL]")
        print(f"  Title: {v2['title']}")
        print(f"  Path: {v2['song_path']}")
        print(f"  Duration: {v2['duration']}s")
        
        print("\n" + "="*70)
        print("[OK] Both versions generated successfully!")
        print("="*70)
        return 0
        
    except (ValueError, RuntimeError, FileNotFoundError) as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
