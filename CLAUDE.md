# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CLI tool to transcribe MP3 audio files to SRT subtitle or plain text format using OpenAI Whisper API (whisper-1).

## Commands

```bash
# Development setup
source venv/bin/activate
pip install -e ".[dev]"

# CI (lint + type-check + test)
make ci

# Individual commands
make lint          # ruff check
make format        # ruff format + check --fix
make type-check    # mypy
make test          # pytest
make test-cov      # pytest with coverage

# Single test execution
pytest tests/unit/domain/test_vocabulary.py -v
pytest tests/unit/infrastructure/test_openai_client.py::test_transcribe_creates_srt_file -v

# Run transcription
python -m transcribe input.mp3                        # Creates SRT
python -m transcribe input.mp3 -o output.srt --language ja  # Japanese SRT
python -m transcribe input.mp3 --text                 # Creates plain text
python -m transcribe --dir ./recordings               # Batch process directory
whisper-srt input.mp3  # After pip install -e .
```

## Architecture

Onion Architecture with Protocol-based dependency injection:

```
src/transcribe/
├── domain/           # Domain layer: vocabulary.py, vocabulary_loader.py
├── application/      # Application layer: protocols.py, batch_processor.py
├── infrastructure/   # Infrastructure layer: openai_client.py (OpenAI Whisper API)
└── interface/        # Interface layer: cli.py (CLI entry point)
```

**Key patterns:**
- `TranscriptionClientProtocol`: Defines transcription client contract with `response_format` parameter. `OpenAITranscriptionClient` implements it
- Response formats: Protocol supports "srt" (subtitles with timestamps) and "text" (plain transcription)
- Vocabulary prompt: `DEFAULT_VOCABULARY` (AI/MCP technical terms) passed to Whisper API's prompt parameter for improved recognition accuracy
- Custom vocabulary: Loaded from `~/.config/whisper-srt/vocabulary.txt` if exists (via `vocabulary_loader.py`)
- CLI `--text` flag: Passes `response_format="text"` to client, outputs plain text instead of SRT subtitles
- CLI `--dir` flag: Batch processes MP3 files in directory recursively via `batch_processor.py`, skips existing outputs

## Testing

- `tests/unit/`: Unit tests
- OpenAI API mocked with `pytest-mock` (no actual API calls)
- Markers: `@pytest.mark.unit`, `@pytest.mark.slow`
