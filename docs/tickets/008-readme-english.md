# Ticket #8: Create English README.md

## Overview
Rewrite README.md in English as the primary documentation for international OSS distribution.

## Acceptance Criteria
- [ ] README.md is entirely in English
- [ ] Installation instructions (pip, pipx)
- [ ] Quick start guide
- [ ] Configuration (API key, vocabulary)
- [ ] Usage examples
- [ ] Supported languages list
- [ ] Contributing section link

## README Structure

```markdown
# whisper-srt

CLI tool to transcribe MP3 audio files to SRT subtitle format using OpenAI Whisper API.

## Features

- Simple CLI for MP3 to SRT conversion
- Automatic language detection or manual specification
- Custom vocabulary support for improved accuracy
- Non-interactive (suitable for batch processing)

## Installation

### Using pipx (Recommended)
\`\`\`bash
pipx install whisper-srt
\`\`\`

### Using pip
\`\`\`bash
pip install whisper-srt
\`\`\`

## Quick Start

1. Set your OpenAI API key:
\`\`\`bash
export OPENAI_API_KEY="your-api-key"
\`\`\`

2. Transcribe an audio file:
\`\`\`bash
whisper-srt audio.mp3
\`\`\`

This creates `audio.srt` in the same directory.

## Usage

\`\`\`bash
# Basic usage (outputs input.srt)
whisper-srt input.mp3

# Specify output file
whisper-srt input.mp3 -o output.srt

# Specify language
whisper-srt input.mp3 --language ja

# Use custom vocabulary file
whisper-srt input.mp3 --vocabulary ~/my-vocab.txt

# Disable vocabulary
whisper-srt input.mp3 --no-vocabulary

# Verbose output
whisper-srt input.mp3 -v
\`\`\`

## Configuration

### API Key
Set `OPENAI_API_KEY` environment variable or create a `.env` file:
\`\`\`
OPENAI_API_KEY=sk-...
\`\`\`

### Custom Vocabulary
Create `~/.config/whisper-srt/vocabulary.txt` with one word per line:
\`\`\`
YouTube
Podcast
Tutorial
# Comments start with #
\`\`\`

## Supported Languages

| Code | Language |
|------|----------|
| en | English (default) |
| ja | Japanese |
| zh | Chinese |
| es | Spanish |
| fr | French |
| de | German |
| ko | Korean |

See [Whisper documentation](https://platform.openai.com/docs/guides/speech-to-text) for full list.

## License

MIT

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.
```

## Files to Modify
- `README.md` - Complete rewrite

## Dependencies
- Should be done after code changes (Phase 1) are complete
- Needed before PyPI publish (Ticket #6)
