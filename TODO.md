# TODO - Beat Addicts: Improve lyric phrasing/structure

- [x] Update `beat_addicts/lyrics_generator.py`
  - [x] Load `rag_data/3_prompt_to_lyrics_guide.txt` and incorporate it into the generation prompt
  - [x] Enforce an output layout (setting line, 2-3 short verse lines, hook near end)
  - [x] Add lightweight post-processing to trim/format lyrics into the expected line structure

- [x] Update `beat_addicts/song_builder.py`
  - [x] Change the lyrics prompt passed to `LyricsGenerator.generate()` to explicitly request verse+hook structure

- [x] Quick manual test
  - [x] Run CLI generation and verify lyric output contains:
    - [x] 1 vivid setting line
    - [x] 2-3 short verse lines
    - [x] a hook-like final line near the end
