import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


class CABCConverter:
    """Converter for Carnatic ABC (CABC) notation to standard ABC notation."""
    
    # Mapping from Carnatic swaras to Western notes
    SWARA_TO_NOTE = {
        'S': 'C', 'R': 'D', 'G': 'E', 'M': 'F',
        'P': 'G', 'D': 'A', 'N': 'B',
        's': 'c', 'r': 'd', 'g': 'e', 'm': 'f',
        'p': 'g', 'd': 'a', 'n': 'b'
    }
    
    # Mapping from Western notes to Carnatic swaras (for swara generation)
    NOTE_TO_SWARA = {
        'C': 'sa', 'D': 'ri', 'E': 'ga', 'F': 'ma',
        'G': 'pa', 'A': 'da', 'B': 'ni',
        'c': 'sa', 'd': 'ri', 'e': 'ga', 'f': 'ma',
        'g': 'pa', 'a': 'da', 'b': 'ni'
    }
    
    def __init__(self):
        """Initialize the CABC converter."""
        self.songs_dir = Path("songs")
    
    def find_cabc_files(self) -> List[Tuple[Path, str]]:
        """
        Find all CABC input files in the songs directory.
        
        Returns:
            List of tuples (file_path, file_type) where file_type is 'notes' or 'notes-lyrics'
        """
        cabc_files = []
        
        for song_dir in self.songs_dir.iterdir():
            if not song_dir.is_dir() or song_dir.name.startswith('_'):
                continue
                
            inputs_dir = song_dir / "inputs"
            if not inputs_dir.exists():
                continue
            
            # Check for notes-only file
            notes_file = inputs_dir / "notes.cabc.abc"
            if notes_file.exists():
                cabc_files.append((notes_file, 'notes'))
            
            # Check for notes with lyrics file
            notes_lyrics_file = inputs_dir / "notes-lyrics.cabc.abc"
            if notes_lyrics_file.exists():
                cabc_files.append((notes_lyrics_file, 'notes-lyrics'))
            
            # Check for notes with lyrics and taala file
            notes_lyrics_taala_file = inputs_dir / "notes-lyrics-taala.cabc.abc"
            if notes_lyrics_taala_file.exists():
                cabc_files.append((notes_lyrics_taala_file, 'notes-lyrics'))
        
        return cabc_files
    
    def convert_cabc_to_abc(self, content: str) -> str:
        """
        Convert CABC notation to standard ABC notation.
        
        Args:
            content: CABC file content
            
        Returns:
            Converted ABC content
        """
        lines = content.split('\n')
        converted_lines = []
        
        for line in lines:
            # Skip empty lines and preserve headers/comments
            if not line.strip() or line.startswith('%') or ':' in line[:10]:
                converted_lines.append(line)
                continue
            
            # Check if it's a lyrics line
            if line.startswith('w:'):
                converted_lines.append(line)
                continue
            
            # Convert music notation line
            converted_line = self._convert_music_line(line)
            converted_lines.append(converted_line)
        
        return '\n'.join(converted_lines)
    
    def _convert_music_line(self, line: str) -> str:
        """
        Convert a single line of CABC music notation to ABC.
        
        Args:
            line: A line containing CABC notation
            
        Returns:
            Converted ABC notation line
        """
        # Pattern to match CABC notes with optional duration and other modifiers
        pattern = r'([SRGMPDNsrgmpdnr])([0-9]*[-]?)'
        
        def replace_note(match):
            swara = match.group(1)
            modifiers = match.group(2)
            
            # Handle rest
            if swara == 'r':
                return 'r' + modifiers
            
            # Convert swara to Western note
            if swara in self.SWARA_TO_NOTE:
                note = self.SWARA_TO_NOTE[swara]
                return note + modifiers
            
            return match.group(0)  # Return unchanged if not recognized
        
        return re.sub(pattern, replace_note, line)
    
    def generate_swaras_for_abc(self, abc_content: str) -> str:
        """
        Generate swara names as lyrics for ABC notation.
        
        Args:
            abc_content: ABC notation content
            
        Returns:
            ABC content with swara names added as lyrics
        """
        lines = abc_content.split('\n')
        result_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            result_lines.append(line)
            
            # Check if this is a music notation line (not header, comment, or lyrics)
            if (line.strip() and 
                not line.startswith('%') and 
                ':' not in line[:10] and 
                not line.startswith('w:')):
                
                # Generate swara line for this music line
                swara_line = self._generate_swara_line(line)
                if swara_line:
                    result_lines.append('w:' + swara_line)
                
                # If there's already a lyrics line after this, add it after the swara line
                if i + 1 < len(lines) and lines[i + 1].startswith('w:'):
                    i += 1
                    result_lines.append(lines[i])
            
            i += 1
        
        return '\n'.join(result_lines)
    
    def _generate_swara_line(self, music_line: str) -> str:
        """
        Generate swara names for a line of ABC music notation.
        
        Args:
            music_line: A line of ABC music notation
            
        Returns:
            Corresponding swara names
        """
        # Pattern to match ABC notes with optional modifiers
        pattern = r"([CDEFGABcdefgabr])([',]*)([0-9]*)([-]?)"
        
        swaras = []
        
        for match in re.finditer(pattern, music_line):
            note = match.group(1)
            # octave = match.group(2)  # Currently not used, but captured for future octave handling
            duration = match.group(3)
            tie = match.group(4)
            
            # Handle rest
            if note == 'r':
                swaras.append('ri')
                continue
            
            # Get swara name
            base_note = note.upper() if note.islower() else note
            if base_note in self.NOTE_TO_SWARA:
                swara = self.NOTE_TO_SWARA[base_note]
                
                # Keep all swaras lowercase (as shown in expected output)
                # This matches the convention in the existing outputs
                
                # Handle tied notes - only show swara for first note
                if tie == '-':
                    swaras.append(swara)
                    # Add continuation marker for the tied note
                    if duration:
                        for _ in range(int(duration) - 1):
                            swaras.append('-')
                else:
                    swaras.append(swara)
                    # Add spacing for longer notes
                    if duration and int(duration) > 1:
                        for _ in range(int(duration) - 1):
                            swaras.append('_')
        
        return ' '.join(swaras)
    
    def process_file(self, input_path: Path, file_type: str = None, output_dir: Path = None):
        """
        Process a single CABC file and generate all required outputs.
        
        Args:
            input_path: Path to the input CABC file
            file_type: Type of file ('notes' or 'notes-lyrics'). If None, detected from filename
            output_dir: Output directory. If None, uses default outputs directory
        """
        # Auto-detect file type if not provided
        if file_type is None:
            if 'notes-lyrics' in input_path.name:
                file_type = 'notes-lyrics'
            else:
                file_type = 'notes'
        
        # Read input file
        with open(input_path, 'r') as f:
            cabc_content = f.read()
        
        # Determine output directory
        if output_dir is None:
            # Default: create outputs directory next to inputs directory
            if input_path.parent.name == 'inputs':
                output_dir = input_path.parent.parent / "outputs"
            else:
                # If not in standard structure, create outputs in same directory
                output_dir = input_path.parent / "outputs"
        
        output_dir.mkdir(exist_ok=True)
        
        # Convert CABC to ABC
        abc_content = self.convert_cabc_to_abc(cabc_content)
        
        # Generate different output files based on file type
        if file_type == 'notes':
            # Generate notes.abc
            notes_output = output_dir / "notes.abc"
            with open(notes_output, 'w') as f:
                f.write(abc_content)
            
            # Generate notes-swaras.abc
            notes_swaras_content = self.generate_swaras_for_abc(abc_content)
            notes_swaras_output = output_dir / "notes-swaras.abc"
            with open(notes_swaras_output, 'w') as f:
                f.write(notes_swaras_content)
                
        elif file_type == 'notes-lyrics':
            # Generate notes-lyrics.abc
            notes_lyrics_output = output_dir / "notes-lyrics.abc"
            with open(notes_lyrics_output, 'w') as f:
                f.write(abc_content)
            
            # Generate notes-swaras-lyrics.abc
            notes_swaras_lyrics_content = self.generate_swaras_for_abc(abc_content)
            notes_swaras_lyrics_output = output_dir / "notes-swaras-lyrics.abc"
            with open(notes_swaras_lyrics_output, 'w') as f:
                f.write(notes_swaras_lyrics_content)
            
            # Also generate notes.abc (without lyrics) and notes-swaras.abc
            abc_no_lyrics = self._remove_lyrics(abc_content)
            
            notes_output = output_dir / "notes.abc"
            with open(notes_output, 'w') as f:
                f.write(abc_no_lyrics)
            
            notes_swaras_content = self.generate_swaras_for_abc(abc_no_lyrics)
            notes_swaras_output = output_dir / "notes-swaras.abc"
            with open(notes_swaras_output, 'w') as f:
                f.write(notes_swaras_content)
    
    def _remove_lyrics(self, abc_content: str) -> str:
        """
        Remove lyrics lines from ABC content.
        
        Args:
            abc_content: ABC content with lyrics
            
        Returns:
            ABC content without lyrics
        """
        lines = abc_content.split('\n')
        return '\n'.join(line for line in lines if not line.startswith('w:'))
    
    def process_all_songs(self):
        """Process all CABC files found in the songs directory."""
        cabc_files = self.find_cabc_files()
        
        if not cabc_files:
            print("No CABC files found in the songs directory.")
            return
        
        print(f"Found {len(cabc_files)} CABC file(s) to process:")
        
        for input_path, file_type in cabc_files:
            song_name = input_path.parent.parent.name
            print(f"\nProcessing {song_name}/{input_path.name} ({file_type})...")
            
            try:
                self.process_file(input_path, file_type)
                print(f"  ✓ Successfully generated outputs for {song_name}")
            except Exception as e:
                print(f"  ✗ Error processing {song_name}: {str(e)}")


def main():
    """Main entry point for carnatic-abc."""
    parser = argparse.ArgumentParser(
        description='Convert Carnatic ABC (CABC) notation to standard ABC notation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  uv run main.py -i songs/sri-govinda/inputs/notes-lyrics.cabc.abc
  uv run main.py -i songs/varaveena/inputs/notes.cabc.abc -o test_outputs/
  uv run main.py --all  # Process all songs
        '''
    )
    
    parser.add_argument('-i', '--input', type=str, 
                        help='Path to input CABC file (e.g., songs/sri-govinda/inputs/notes-lyrics.cabc.abc)')
    parser.add_argument('-o', '--output', type=str, 
                        help='Output directory (default: creates outputs/ next to inputs/)')
    parser.add_argument('--all', action='store_true',
                        help='Process all songs in the songs directory')
    
    args = parser.parse_args()
    
    converter = CABCConverter()
    
    if args.all:
        # Process all songs
        converter.process_all_songs()
    elif args.input:
        # Process single file
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' does not exist")
            sys.exit(1)
        
        if not input_path.name.endswith('.cabc.abc'):
            print(f"Error: Input file must have .cabc.abc extension")
            sys.exit(1)
        
        output_dir = Path(args.output) if args.output else None
        
        print(f"Processing {input_path}...")
        try:
            converter.process_file(input_path, output_dir=output_dir)
            print(f"✓ Successfully generated outputs")
            if output_dir:
                print(f"  Output directory: {output_dir}")
        except Exception as e:
            print(f"✗ Error processing file: {str(e)}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()