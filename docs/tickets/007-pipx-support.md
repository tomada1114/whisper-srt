# Ticket #7: pipx Support Verification

## Overview
Verify and document that the package works correctly with pipx for isolated CLI installation.

## Acceptance Criteria
- [ ] `pipx install whisper-srt` works correctly
- [ ] CLI commands work after pipx installation
- [ ] Environment variables are properly accessible
- [ ] Documentation includes pipx installation instructions

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
