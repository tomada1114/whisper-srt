# Ticket #5: Convert Codebase to English

## Overview
Convert all Japanese comments, docstrings, and error messages to English for international OSS distribution.

## Acceptance Criteria
- [ ] All docstrings in English
- [ ] All inline comments in English
- [ ] All error messages in English
- [ ] All log messages in English
- [ ] CLAUDE.md remains in Japanese (project-internal file)

## Files to Review and Update

### `src/transcribe/domain/vocabulary.py`
- Remove Japanese category comments
- Update module docstring

### `src/transcribe/infrastructure/openai_client.py`
- Module docstring (already English)
- Verify all comments are English

### `src/transcribe/interface/cli.py`
- Help text (already English)
- Error messages (verify)

### `src/transcribe/application/protocols.py`
- Docstrings (already English)

### Test files
- Test names and docstrings should be English

## Example Changes

### Before (Japanese)
```python
# AI サービス・プラットフォーム
AI_SERVICES: tuple[str, ...] = (...)
```

### After (English)
```python
# AI services and platforms
AI_SERVICES: tuple[str, ...] = (...)
```

## Verification
```bash
# Search for remaining Japanese characters
grep -r '[ぁ-んァ-ン一-龯]' src/
```

## Dependencies
- None (can be done in parallel with Phase 1 tickets)
- Should be completed before README updates
