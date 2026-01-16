# whisper-srt

CLI tool to transcribe MP3 audio files to SRT subtitle or plain text format using OpenAI Whisper API.

English | [日本語](https://github.com/tomada1114/whisper-srt/blob/main/README.ja.md)

## Features

- Simple CLI for MP3 to SRT or plain text conversion
- High-accuracy transcription via OpenAI Whisper API (`whisper-1`)
- Built-in AI/tech terminology for better recognition
- Custom vocabulary support
- Output as SRT subtitles or plain text

## Quick Start

**No installation required** - just run with [uv](https://docs.astral.sh/uv/):

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key"

# Transcribe (creates audio.srt)
uvx whisper-srt audio.mp3
```

Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys).

## Installation (Optional)

If you prefer a permanent install:

```bash
uv tool install whisper-srt
whisper-srt audio.mp3
```

> **Note**: If you see `Executable already exists` error, use `--force` to overwrite:
> ```bash
> uv tool install whisper-srt --force
> ```

## Upgrade

If you have whisper-srt installed, upgrade to the latest version:

```bash
uv tool upgrade whisper-srt
```

## Usage

```bash
whisper-srt input.mp3                    # Basic usage (creates input.srt)
whisper-srt input.mp3 -o output.srt      # Specify output file
whisper-srt input.mp3 --language ja      # Specify language (Japanese)
whisper-srt input.mp3 --text             # Output as plain text (creates input.txt)
whisper-srt --help                       # See all options
```

### Output Formats

By default, transcription is saved as **SRT subtitle format** with timestamps. Use `--text` to save as plain text instead:

```bash
whisper-srt audio.mp3              # Creates: audio.srt (subtitle format)
whisper-srt audio.mp3 --text       # Creates: audio.txt (plain text)
whisper-srt audio.mp3 --text -o output.txt  # Custom output path with text format
```

## Initial Setup

Run `--init` to configure default settings interactively:

```bash
whisper-srt --init
```

This command:
1. Creates a vocabulary file at `~/.config/whisper-srt/vocabulary.txt`
2. Prompts you to select a default language (saved to `~/.config/whisper-srt/language.txt`)

After setup, you can skip the `--language` option for everyday use.

## Supported Languages

Default language is **English (`en`)**.

Common language codes (ISO-639-1):
| Code | Language | Code | Language |
|------|----------|------|----------|
| `en` | English | `ja` | Japanese |
| `zh` | Chinese | `ko` | Korean |
| `es` | Spanish | `fr` | French |
| `de` | German | `pt` | Portuguese |

See [OpenAI Whisper documentation](https://platform.openai.com/docs/guides/speech-to-text) for all supported languages.

## Custom Vocabulary

Create `~/.config/whisper-srt/vocabulary.txt` with domain-specific terms:

```
YouTube
Podcast
MyCompanyName
```

## Pricing

$0.006/minute (~$0.36/hour)

## Development

```bash
git clone https://github.com/tomada1114/whisper-srt.git
cd whisper-srt
uv sync --dev
make ci   # lint + type-check + test
```

## License

MIT
