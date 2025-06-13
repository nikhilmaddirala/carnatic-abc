# carnatic-abc
Tools for working with Carnatic music in ABC notation.

## Folder Structure
songs/song_name
- transcription.cabc: manual transcription of the song in Carnatic ABC notation provided by the user as input.

## Features
- Generate ABC notes from cabc notes
- 


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
