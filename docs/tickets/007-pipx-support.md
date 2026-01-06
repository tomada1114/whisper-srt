# Ticket #7: pipx Support Verification

## Overview
Verify and document that the package works correctly with pipx for isolated CLI installation.

## Acceptance Criteria
- [x] `pipx install whisper-srt` works correctly
- [x] CLI commands work after pipx installation
- [x] Environment variables are properly accessible
- [x] Documentation includes pipx installation instructions

## Testing Steps

### Install via pipx
```bash
# Install pipx if not already installed
pip install pipx
pipx ensurepath

# Install whisper-srt
pipx install whisper-srt

# Verify installation
whisper-srt --version
whisper-srt --help
```

### Test Functionality
```bash
# Set API key
export OPENAI_API_KEY="your-api-key"

# Test transcription
whisper-srt test.mp3
```

### Test with Custom Vocabulary
```bash
# Create vocabulary file
mkdir -p ~/.config/whisper-srt
echo "CustomWord" > ~/.config/whisper-srt/vocabulary.txt

# Test that vocabulary is loaded
whisper-srt test.mp3 -v
```

## Potential Issues to Address

### Issue 1: dotenv in pipx environment
The tool uses `python-dotenv` to load `.env` files. Verify this works correctly in pipx's isolated environment.

### Issue 2: Config directory access
Ensure `~/.config/whisper-srt/` is accessible from pipx-installed package.

## Documentation Update
Add to README.md:

```markdown
## Installation

### Using pipx (Recommended)
pipx provides isolated installation, avoiding dependency conflicts:

```bash
pipx install whisper-srt
```

### Using pip
```bash
pip install whisper-srt
```
```

## Dependencies
- Ticket #6 (PyPI publish) must be completed first
- Package must be available on PyPI for pipx installation

## Completion Notes (2025-01-06)

### Verified
- `pipx install whisper-srt` successfully installs v0.2.0
- `whisper-srt --version` and `whisper-srt --help` work correctly
- Environment variable `OPENAI_API_KEY` is accessible
- `~/.config/whisper-srt/vocabulary.txt` is accessible via `Path.home()`
- `load_dotenv()` works from current working directory

### Documentation Added
- PyPI publishing guide: `docs/publishing-guide.md`
- README.md updated with pipx/pip installation instructions
- API key setup clarified (environment variable vs .env file)
