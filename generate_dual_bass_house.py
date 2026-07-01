"""
Generate 2 related high-energy bass house tracks with surprise elements
Both versions inspired by LEVITY - Flip It & FISHER sound
Version 1: High-Energy Bass House with Explosive Drops
Version 2: Experimental Bass House with Complex Buildups
"""

import os
import sys
import json
import time
from typing import Dict, Tuple
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from beat_addicts.song_builder_addiction import AddictionFormulaSongBuilder


class DualBassHouseGenerator:
    """Generates two related bass house tracks with different AF strategies"""
    
    def __init__(self, output_base="output"):
        self.output_base = output_base
        self.builder = AddictionFormulaSongBuilder(output_dir=output_base)
        self.session_timestamp = int(time.time())
    
    def generate_dual_tracks(self) -> Tuple[Dict, Dict]:
        """Generate 2 related bass house tracks in sequence"""
        
        print("\n" + "="*70)
        print("DUAL BASS HOUSE GENERATION: LEVITY × FISHER")
        print("="*70)
        
        # Version 1: High-Energy Bass House with Explosive Drops
        print("\n[VERSION 1] Generating: High-Energy Bass House with Explosive Drops...")
        print("-" * 70)
        
        version_1_prompt = (
            "High-energy bass house track inspired by LEVITY Flip It and FISHER. "
            "Start with deep filtered bass synth pad with side-chain compression. "
            "Add punchy 808 kicks on downbeats. Layered Hi-Hat rolls every 8 bars. "
            "Big surprise drop at 0:30 - sudden stop to silence, then explosive bass punch. "
            "Wobble bass LFO automation for tension. "
            "Experimental filtered vocal chops as texture layer. "
            "Build to climax with accelerating percussion fills. "
            "Use only electronic/synth instruments. Keep it club-ready and bass-focused."
        )
        
        version_1 = self.builder.build_song_with_addiction_formula(
            prompt=version_1_prompt,
            genre="bass_house",
            duration=45,  # Longer for extended club mix
            progress_callback=self._progress_v1,
            enable_composition_scoring=True
        )
        
        print(f"✓ Version 1 Complete: {version_1['song_path']}")
        
        # Version 2: Experimental Bass House with Complex Buildups
        print("\n[VERSION 2] Generating: Experimental Bass House with Complex Buildups...")
        print("-" * 70)
        
        version_2_prompt = (
            "Experimental bass house with FISHER's unpredictable production style. "
            "Open with sparse pad and reverb-heavy filtered bass drone. "
            "Introduce clipped snare breaks at unexpected intervals (not 4/4). "
            "Layer 1: Polyrhythmic percussion (swung 16ths against straight 8ths). "
            "Layer 2: Granular synth textures with random cutoff automation. "
            "Mid-track surprise: tempo shift down 5 BPM, then snap back with filter sweep. "
            "Use vocal glitches as rhythmic element, not melody. "
            "Build complexity through production layers, not volume. "
            "Finish with semi-resolved ending (ambiguous, leaves question mark). "
            "Maximum creative production, experimental texture focus."
        )
        
        version_2 = self.builder.build_song_with_addiction_formula(
            prompt=version_2_prompt,
            genre="experimental_bass",
            duration=50,  # Slightly longer for experimental development
            progress_callback=self._progress_v2,
            enable_composition_scoring=True
        )
        
        print(f"✓ Version 2 Complete: {version_2['song_path']}")
        
        # Create comparison report
        self._create_comparison_report(version_1, version_2)
        
        return version_1, version_2
    
    def _progress_v1(self, percent: int):
        """Progress callback for Version 1"""
        bar_length = 40
        filled = int(bar_length * percent / 100)
        bar = "=" * filled + "-" * (bar_length - filled)
        print(f"\r[V1] {bar} {percent}%", end="", flush=True)
    
    def _progress_v2(self, percent: int):
        """Progress callback for Version 2"""
        bar_length = 40
        filled = int(bar_length * percent / 100)
        bar = "=" * filled + "-" * (bar_length - filled)
        print(f"\r[V2] {bar} {percent}%", end="", flush=True)
    
    def _create_comparison_report(self, v1: Dict, v2: Dict):
        """Create side-by-side comparison of both versions"""
        
        report = {
            "generation_session": self.session_timestamp,
            "customer_request": "High-energy bass house cross between LEVITY - Flip It & FISHER, experimental, surprise elements",
            
            "version_1": {
                "title": "High-Energy Bass House with Explosive Drops",
                "strategy": "AF Surprise Transition + Volume-Based Hype Control",
                "song_id": v1['song_id'],
                "song_path": v1['song_path'],
                "lyrics_path": v1['lyrics_path'],
                "analysis_path": v1['analysis_path'],
                "duration": v1['duration'],
                "composition_score": v1['composition_score'],
                "key_techniques": [
                    "Filtered bass pad with side-chain compression",
                    "Surprise Drop transition (silence => explosive bass)",
                    "Wobble bass LFO for tension creation",
                    "Accelerating percussion fills (rhythm-based hype)",
                    "808 kicks + hi-hat rolls (arrangement-based hype)",
                    "Vocal chops as textural layer (novelty hype)",
                ],
                "energy_curve_strategy": "Standard 3-peak with emphasis on 0:30 Surprise drop",
                "af_transitions": [
                    "Start: Smooth fade-in (low hype to mid)",
                    "0:20: Lift transition (tension building)",
                    "0:30: SURPRISE transition (silent drop, resets, explosive return)",
                    "1:00: Overshoot transition (peak higher than expected)",
                    "End: False Promise (almost finish, 1 more build)"
                ]
            },
            
            "version_2": {
                "title": "Experimental Bass House with Complex Buildups",
                "strategy": "AF Implied Tension + Production-Based Energy Shifts",
                "song_id": v2['song_id'],
                "song_path": v2['song_path'],
                "lyrics_path": v2['lyrics_path'],
                "analysis_path": v2['analysis_path'],
                "duration": v2['duration'],
                "composition_score": v2['composition_score'],
                "key_techniques": [
                    "Polyrhythmic percussion (breaks 4/4 predictability)",
                    "Granular synth textures with random automation",
                    "Tempo shift surprise (down 5 BPM mid-track)",
                    "Vocal glitches as rhythmic puzzle (not melody)",
                    "Production layers increase complexity, not volume",
                    "Semi-resolved ending (ambiguous, implied tension)",
                ],
                "energy_curve_strategy": "Non-linear 3-peak with complexity crescendo",
                "af_transitions": [
                    "Start: Flatline (low energy, waiting)",
                    "0:15: Lift (tension builds through texture, not volume)",
                    "0:45: Negative Tension (tempo drop creates disorientation)",
                    "1:00: Jump (snap back, filter sweep uplifter)",
                    "End: Negative Tension (leaves unresolved question)"
                ]
            },
            
            "comparison": {
                "v1_focuses_on": "High-energy maximization, explosive drops, club-ready impact, traditional energy curves",
                "v2_focuses_on": "Complexity, listener engagement through confusion/resolution, production-forward storytelling, experimental grooves",
                "shared_elements": [
                    "Bass house foundation (deep filtered basses, 808s)",
                    "LEVITY & FISHER inspiration (high production quality)",
                    "Surprise elements (both use AF Surprise/Negative Tension)",
                    "Electronic instrumentation only",
                    "Club-viable lengths (45-50 seconds)"
                ],
                "use_case_v1": "DJ sets, club peak time, dance floor energy maximization",
                "use_case_v2": "Chill club moments, underground venue showcase, production portfolio, listener intrigue"
            }
        }
        
        # Save comparison report
        report_path = os.path.join(self.output_base, f"dual_generation_{self.session_timestamp}.json")
        with open(report_path, "w", encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print("\n" + "="*70)
        print("GENERATION COMPLETE")
        print("="*70)
        print(f"\n[REPORT] Comparison saved: {report_path}")
        print(f"\n[V1 - HIGH-ENERGY] {v1['song_path']}")
        print(f"   Score: {v1['composition_score']}")
        print(f"   Duration: {v1['duration']}s")
        print(f"\n[V2 - EXPERIMENTAL] {v2['song_path']}")
        print(f"   Score: {v2['composition_score']}")
        print(f"   Duration: {v2['duration']}s")
        print("\n" + "="*70)


def main():
    """Main entry point"""
    try:
        generator = DualBassHouseGenerator(output_base="output")
        _, _ = generator.generate_dual_tracks()
        
        print("\n[OK] SUCCESS: Both tracks generated and compared")
        return 0
        
    except (ValueError, RuntimeError, FileNotFoundError) as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
