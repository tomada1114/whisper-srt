# whisper-srt

CLI tool to transcribe MP3 audio files to SRT subtitle format using OpenAI Whisper API.

English | [日本語](README.ja.md)

## Features

- Simple CLI for MP3 to SRT conversion
- High-accuracy transcription via OpenAI Whisper API (`whisper-1`)
- Automatic language detection or manual specification
- Custom vocabulary support for improved accuracy
- Built-in AI/tech terminology for better recognition
- Non-interactive mode suitable for batch processing

## Pricing

- $0.006/minute (approximately $0.36/hour)
- New OpenAI accounts receive free credits

## Installation

### Using pipx (Recommended)

Install in an isolated environment to avoid dependency conflicts:

```bash
pipx install whisper-srt
```

### Using pip

```bash
pip install whisper-srt
```

### From Source (Development)

```bash
git clone https://github.com/tomada1114/whisper-srt.git
cd whisper-srt
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## Quick Start

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key"
```

2. Transcribe an audio file:
```bash
whisper-srt audio.mp3
```

This creates `audio.srt` in the same directory.

## Usage

```bash
# Basic usage (outputs input.srt)
whisper-srt input.mp3

# Specify output file
whisper-srt input.mp3 -o output.srt

# Specify language (ISO-639-1 code)
whisper-srt input.mp3 --language ja

# Use custom vocabulary file
whisper-srt input.mp3 --vocabulary ~/my-vocab.txt

# Disable vocabulary
whisper-srt input.mp3 --no-vocabulary

# Verbose output
whisper-srt input.mp3 -v
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output SRT file path | `{input_filename}.srt` |
| `--language` | Language code (ISO-639-1) | `ja` |
| `--vocabulary` | Custom vocabulary file path | None |
| `--no-vocabulary` | Disable all vocabulary prompts | Off |
| `-v, --verbose` | Enable verbose logging | Off |

## Configuration

### API Key

Set your OpenAI API key using one of these methods:

#### Method 1: Environment Variable (Recommended for pipx)

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

Add to your shell config (`~/.zshrc` or `~/.bashrc`) to persist.

#### Method 2: .env File (Per-project)

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY
```

Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys).

### Custom Vocabulary

Create `~/.config/whisper-srt/vocabulary.txt` with one word per line:

```
YouTube
Podcast
Tutorial
# Comments start with #
```

### Built-in Vocabulary

The following AI/tech terminology categories are built-in to improve recognition accuracy:

- AI Services (Claude, ChatGPT, Gemini, etc.)
- AI Coding Tools (Cursor, Windsurf, Cline, etc.)
- MCP (Model Context Protocol, MCP Connector, etc.)
- Claude Code Features (CLAUDE.md, sub-agents, hooks, etc.)
- Development Methodologies (DDD, Onion Architecture, AI-driven development, etc.)

## Supported Languages

| Code | Language |
|------|----------|
| en | English |
| ja | Japanese (default) |
| zh | Chinese |
| es | Spanish |
| fr | French |
| de | German |
| ko | Korean |

See [Whisper documentation](https://platform.openai.com/docs/guides/speech-to-text) for the full list of supported languages.

## Development

```bash
make help        # Show help
make ci          # Run lint + type-check + test
make test        # Run tests
make test-cov    # Run tests with coverage
make lint        # Run linter
make format      # Format code
make type-check  # Run type checker
```

## Dependencies

- Python 3.9+
- openai
- python-dotenv

## License

MIT

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.
