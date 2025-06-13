# Tests

This directory contains pytest-based tests for the carnatic-abc converter.

## Structure

- `test_converter.py`: Unit tests for the CABC converter
- `fixtures/`: Test data and sample files
  - `sri-govinda/`: Sample song for integration testing

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output and show print statements
uv run pytest -v -s

# Run specific test file
uv run pytest tests/test_converter.py

# Run specific test
uv run pytest tests/test_converter.py::TestCABCConverter::test_swara_to_note_mapping
```

## Test Coverage

The tests cover:
- Basic swara to note mapping
- Note sequence conversion
- Duration and tie handling
- Header preservation
- Swara generation
- File-based integration testing
- Real song conversion with sri-govinda fixture

## Understanding Test Output

When you run tests with `-s` flag, you'll see:
- Input CABC notation and output ABC notation for conversions
- Generated swara lines
- Full file conversion results including all output files

This helps verify the converter is working correctly and understand what transformations are happening.