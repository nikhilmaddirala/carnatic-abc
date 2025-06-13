# carnatic-abc
Tools for working with Carnatic music in ABC notation.

## How to use this
- Provide your input either as `songs/song_name/input/notes.cabc.abc` or `songs/song_name/input/notes-lyrics.cabc.abc`
    - find a source online and transcribe the song into cabc notation
    - make sure to map it onto a western time signature
    - make sure you get the lyrics right as per abc notation
- Run the python main script to generate the outputs.
- If you provided `songs/song_name/notes.cabc.abc` as input, the following outputs will be generated:
    - `songs/song_name/output/notes-swaras.abc`
    - `songs/song_name/output/notes.abc`
- If you provided `songs/song_name/notes-lyrics.cabc.abc` as input, the following additional outputs will be generated in addition to the above:
    - `songs/song_name/output/notes-lyrics-swaras.abc`
    - `songs/song_name/output/notes-lyrics.abc`

## Future roadmap
- Implement main.py with pytest framework
- Convert abc to musicxml / musescore notation
- Create web app to visualize and play the musicxml
- Automatic transcription of cabc from source PDF
