import torch

import sys
from pathlib import Path

# Add parent directory to path (safer implementation)
sys.path.insert(0, str(Path(__file__).parent.parent))

import click
from beat_addicts.song_builder import SongBuilder

@click.command()
@click.argument("prompt")
@click.option("--duration", default=15,
             help="Duration (5-90s) on CPU, longer with GPU",
             type=click.IntRange(5, 90))
@click.option("--output", default="output",
             help="Output directory (will be created)")
def generate_song(prompt, duration, output):
    """Generate complete songs using best available device (GPU if available)."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    click.echo(f"\n[*] Device Mode ({device}) | Generating {duration}s song... (Max threads: {torch.get_num_threads()})")

    try:
        builder = SongBuilder(output_dir=output)
        with click.progressbar(length=100, label='Generating') as bar:
            result = builder.build_song(prompt, duration)
            bar.update(100)

        click.secho("\n[+] Generation Complete!", fg="green")
        click.echo(f"[*] Title: {result['title']}")
        click.echo(f"[*] Lyrics: {file_link(result['lyrics_path'])}")
        click.echo(f"[*] Audio: {file_link(result['song_path'])}")
    except Exception as e:
        click.secho(f"\n[!] Error: {str(e)}", fg="red")
        if "memory" in str(e).lower():
            click.echo("[*] Try reducing --duration or using simpler prompts")

def file_link(path):
    """Convert file path to clickable link in supported terminals"""
    return f"\033]8;;file://{Path(path).absolute()}\a{path}\033]8;;\a"

if __name__ == "__main__":
    generate_song()
