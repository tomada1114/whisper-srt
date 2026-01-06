# Ticket #4: Vocabulary File Loading Feature

## Overview
Add ability to load custom vocabulary from a text file. The tool will automatically look for `~/.config/whisper-srt/vocabulary.txt` and use it if present.

## Acceptance Criteria
- [ ] Automatically load `~/.config/whisper-srt/vocabulary.txt` if it exists
- [ ] If file doesn't exist, run without vocabulary (no error)
- [ ] `--vocabulary /path/to/file.txt` option to specify custom file
- [ ] `--no-vocabulary` option to disable vocabulary loading entirely
- [ ] File format: one word per line, UTF-8 encoding
- [ ] Empty lines and lines starting with `#` are ignored
- [ ] Tests cover all scenarios

## Implementation

### New File: `src/transcribe/domain/vocabulary_loader.py`
```python
"""Vocabulary file loader.

Loads custom vocabulary from text files for Whisper API prompt.
"""

from pathlib import Path

DEFAULT_VOCABULARY_PATH = Path.home() / ".config" / "whisper-srt" / "vocabulary.txt"


def load_vocabulary_from_file(path: Path) -> tuple[str, ...]:
    """Load vocabulary from a text file.

    Args:
        path: Path to vocabulary file (one word per line)

    Returns:
        Tuple of vocabulary terms

    Raises:
        FileNotFoundError: If file does not exist
    """
    if not path.exists():
        raise FileNotFoundError(f"Vocabulary file not found: {path}")

    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        # Skip empty lines and comments
        if line and not line.startswith("#"):
            terms.append(line)

    return tuple(terms)


def load_default_vocabulary() -> tuple[str, ...]:
    """Load vocabulary from default location if it exists.

    Returns:
        Tuple of vocabulary terms, or empty tuple if file not found
    """
    if DEFAULT_VOCABULARY_PATH.exists():
        return load_vocabulary_from_file(DEFAULT_VOCABULARY_PATH)
    return ()
```

### Modify: `src/transcribe/interface/cli.py`
```python
# Add to argument parser
vocab_group = parser.add_mutually_exclusive_group()
vocab_group.add_argument(
    "--vocabulary",
    type=Path,
    default=None,
    help="Path to vocabulary file (one word per line)",
)
vocab_group.add_argument(
    "--no-vocabulary",
    action="store_true",
    help="Disable vocabulary loading",
)

# In main():
if args.no_vocabulary:
    vocabulary = ()
elif args.vocabulary:
    vocabulary = load_vocabulary_from_file(args.vocabulary)
else:
    vocabulary = load_default_vocabulary()

client = OpenAITranscriptionClient(language=args.language, vocabulary=vocabulary)
```

## File Format Example
`~/.config/whisper-srt/vocabulary.txt`:
```
# Custom vocabulary for transcription
# One word or phrase per line

YouTube
TikTok
Instagram
Podcast
Tutorial
Subscribe
Like and Share
```

## Testing
```python
def test_load_vocabulary_from_file(tmp_path):
    vocab_file = tmp_path / "vocab.txt"
    vocab_file.write_text("word1\nword2\n# comment\n\nword3")

    result = load_vocabulary_from_file(vocab_file)

    assert result == ("word1", "word2", "word3")

def test_load_vocabulary_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_vocabulary_from_file(Path("/nonexistent/file.txt"))

def test_load_default_vocabulary_returns_empty_when_no_file():
    # Mock DEFAULT_VOCABULARY_PATH to non-existent path
    result = load_default_vocabulary()
    assert result == ()
```

## Dependencies
- Ticket #3 (vocabulary.py refactor) should be completed first
