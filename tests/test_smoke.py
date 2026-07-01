from pathlib import Path

import pytest

from beat_addicts import cli
from beat_addicts.addiction_formula import TransitionType
import beat_addicts.melody_generator as melody_generator


def test_transition_enum_exposes_expected_value() -> None:
    assert TransitionType.JUMP.value == "jump"


def test_file_link_includes_absolute_file_uri() -> None:
    link = cli.file_link("output/song.mp3")
    assert "file://" in link
    assert str(Path("output/song.mp3")) in link


def test_melody_generator_raises_when_audiocraft_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(melody_generator, "AUDIOCRAFT_AVAILABLE", False)
    with pytest.raises(ImportError):
        melody_generator.MelodyGenerator()
