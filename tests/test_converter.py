import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import CABCConverter


class TestCABCConverter:
    """Test suite for CABC to ABC converter."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.converter = CABCConverter()
    
    def test_swara_to_note_mapping(self):
        """Test basic swara to Western note conversion."""
        assert self.converter.SWARA_TO_NOTE['S'] == 'C'
        assert self.converter.SWARA_TO_NOTE['R'] == 'D'
        assert self.converter.SWARA_TO_NOTE['G'] == 'E'
        assert self.converter.SWARA_TO_NOTE['s'] == 'c'
        assert self.converter.SWARA_TO_NOTE['r'] == 'd'
    
    def test_convert_single_note(self):
        """Test conversion of single notes."""
        assert self.converter.convert_cabc_to_abc("S") == "C"
        assert self.converter.convert_cabc_to_abc("s") == "c"
        assert self.converter.convert_cabc_to_abc("R") == "D"
        assert self.converter.convert_cabc_to_abc("r") == "r"  # rest should stay as rest
    
    def test_convert_note_sequence(self):
        """Test conversion of note sequences."""
        input_cabc = "S R G M | P D N s |"
        expected = "C D E F | G A B c |"
        result = self.converter.convert_cabc_to_abc(input_cabc)
        
        print(f"\nNote sequence conversion:")
        print(f"  Input CABC: {input_cabc}")
        print(f"  Output ABC: {result}")
        
        assert result == expected
    
    def test_convert_with_duration(self):
        """Test conversion with note durations."""
        input_cabc = "S2 R4 G- | -G M P2 |"
        expected = "C2 D4 E- | -E F G2 |"
        assert self.converter.convert_cabc_to_abc(input_cabc) == expected
    
    def test_preserve_headers(self):
        """Test that ABC headers are preserved."""
        input_cabc = """X:1
T:Test Song
M:4/4
L:1/4
K:C
S R G M |"""
        
        output = self.converter.convert_cabc_to_abc(input_cabc)
        assert "X:1" in output
        assert "T:Test Song" in output
        assert "M:4/4" in output
        assert "C D E F |" in output
    
    def test_generate_swaras_simple(self):
        """Test swara generation for simple ABC notation."""
        abc_content = "C D E F |"
        expected_swaras = "sa ri ga ma"
        
        swara_line = self.converter._generate_swara_line(abc_content)
        
        print(f"\nSwara generation:")
        print(f"  Input ABC:  {abc_content}")
        print(f"  Output Swaras: {swara_line}")
        
        assert swara_line == expected_swaras
    
    def test_generate_swaras_with_rest(self):
        """Test swara generation with rests."""
        abc_content = "C r D E |"
        expected_swaras = "sa ri ri ga"
        
        swara_line = self.converter._generate_swara_line(abc_content)
        assert swara_line == expected_swaras


# Integration test
def test_file_conversion(tmp_path):
    """Test full file conversion process."""
    converter = CABCConverter()
    
    # Create test input file
    input_dir = tmp_path / "inputs"
    input_dir.mkdir()
    
    test_cabc = """X:1
T:Test Song
M:4/4
L:1/4
K:C
S R G M | P D N s |
w:sa ri ga ma pa da ni sa"""
    
    input_file = input_dir / "notes-lyrics.cabc.abc"
    input_file.write_text(test_cabc)
    
    print(f"\n{'='*60}")
    print("FULL FILE CONVERSION TEST")
    print(f"{'='*60}")
    print(f"\nInput CABC file content:")
    print(test_cabc)
    
    # Process file
    converter.process_file(input_file, output_dir=tmp_path / "outputs")
    
    # Check outputs exist
    output_dir = tmp_path / "outputs"
    assert output_dir.exists()
    assert (output_dir / "notes-lyrics.abc").exists()
    assert (output_dir / "notes-swaras-lyrics.abc").exists()
    
    # Check and display content
    notes_abc = (output_dir / "notes-lyrics.abc").read_text()
    print(f"\nOutput notes-lyrics.abc:")
    print(notes_abc)
    
    notes_swaras = (output_dir / "notes-swaras-lyrics.abc").read_text()
    print(f"\nOutput notes-swaras-lyrics.abc:")
    print(notes_swaras)
    
    assert "C D E F | G A B c |" in notes_abc
    assert "w:sa ri ga ma pa da ni sa" in notes_abc


def test_real_song_conversion():
    """Test conversion with real song from fixtures."""
    converter = CABCConverter()
    fixture_path = Path(__file__).parent / "fixtures" / "sri-govinda" / "inputs" / "notes-lyrics.cabc.abc"
    
    if not fixture_path.exists():
        pytest.skip("Fixture file not found")
    
    print(f"\n{'='*60}")
    print("REAL SONG CONVERSION TEST: Sri Govinda")
    print(f"{'='*60}")
    
    # Read input
    cabc_content = fixture_path.read_text()
    print(f"\nInput CABC (first 10 lines):")
    print('\n'.join(cabc_content.split('\n')[:10]))
    
    # Convert
    abc_content = converter.convert_cabc_to_abc(cabc_content)
    print(f"\nConverted ABC (first 10 lines):")
    print('\n'.join(abc_content.split('\n')[:10]))
    
    # Generate swaras
    abc_with_swaras = converter.generate_swaras_for_abc(abc_content)
    print(f"\nWith Swaras (lines 6-15):")
    lines = abc_with_swaras.split('\n')
    print('\n'.join(lines[5:15]))
    
    # Basic assertions
    assert "c B c2 | A B | c B A G |" in abc_content
    assert "w: sri _ go vin _ da _ _ _" in abc_content