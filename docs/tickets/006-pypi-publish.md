# Ticket #6: PyPI Publish Preparation

## Overview
Prepare the package for PyPI publication so users can install via `pip install whisper-srt`.

## Acceptance Criteria
- [x] `pyproject.toml` metadata complete
- [x] Package builds successfully
- [x] README.md displays correctly on PyPI
- [x] GitHub Actions workflow for automated publishing
- [ ] Package successfully uploaded to PyPI

## Implementation

### Update `pyproject.toml`

```toml
[project]
name = "whisper-srt"
version = "0.2.0"  # Increment for new features
description = "CLI tool to transcribe MP3 audio to SRT subtitles using OpenAI Whisper API"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "tomada1114", email = "tmasuyama1114@gmail.com"}
]
keywords = ["transcription", "whisper", "srt", "subtitles", "audio", "openai"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Multimedia :: Sound/Audio :: Speech",
]

[project.urls]
Homepage = "https://github.com/tomada1114/whisper-srt"
Repository = "https://github.com/tomada1114/whisper-srt"
Issues = "https://github.com/tomada1114/whisper-srt/issues"
```

### Create `.github/workflows/publish.yml`

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install build tools
        run: pip install build

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

### Manual First Publish
```bash
# Build
pip install build
python -m build

# Upload to PyPI (requires API token)
pip install twine
twine upload dist/*
```

## Pre-publish Checklist
- [x] Version number updated (0.1.0 → 0.2.0)
- [x] README.md is complete and renders correctly
- [x] All tests pass (`make ci`)
- [x] Package installs correctly locally (`pip install .`)
- [x] CLI works after installation (`whisper-srt --version`)

## Dependencies
- Ticket #8 (README.md in English) should be completed first
