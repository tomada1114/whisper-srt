# Ticket #3: Refactor vocabulary.py

## Overview
Simplify the vocabulary module by removing category-based organization. The built-in vocabulary will become an empty tuple, as vocabulary loading will be handled by the new vocabulary file feature.

## Acceptance Criteria
- [ ] `DEFAULT_VOCABULARY` changed to empty tuple `()`
- [ ] Category definitions removed or archived
- [ ] `build_vocabulary()` function removed (no longer needed)
- [ ] Tests updated to reflect new behavior
- [ ] No breaking changes to `OpenAITranscriptionClient` interface

## Implementation

### Files to Modify

#### `src/transcribe/domain/vocabulary.py`
```python
"""Default vocabulary for transcription.

The built-in vocabulary is empty. Users can provide custom vocabulary
via ~/.config/whisper-srt/vocabulary.txt or --vocabulary option.
"""

# Empty by default - users provide their own vocabulary
DEFAULT_VOCABULARY: tuple[str, ...] = ()
```

#### `src/transcribe/domain/__init__.py`
- Keep exporting `DEFAULT_VOCABULARY`

### Archive Decision
The existing category definitions (AI_SERVICES, CODING_TOOLS, etc.) should be:
- Option A: Delete completely (recommended for clean codebase)
- Option B: Move to `docs/examples/vocabulary-ai-development.txt` as reference

## Testing
```python
from transcribe.domain.vocabulary import DEFAULT_VOCABULARY

def test_default_vocabulary_is_empty():
    assert DEFAULT_VOCABULARY == ()
```

## Dependencies
- None (can be implemented independently)
- Should be completed before Ticket #4 (vocabulary file loading)
