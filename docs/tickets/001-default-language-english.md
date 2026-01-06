# Ticket #1: Change Default Language to English

## Overview
Change the default transcription language from Japanese (`ja`) to English (`en`) to make the tool more accessible for international users.

## Acceptance Criteria
- [ ] Default language in CLI is `en` instead of `ja`
- [ ] `--language` option still works for specifying other languages
- [ ] Help text updated to reflect new default
- [ ] Tests updated for new default behavior

## Implementation

### Files to Modify
- `src/transcribe/interface/cli.py`
  - Change `default="ja"` to `default="en"` in argparse
  - Update help text

### Supported Languages
Document these commonly used language codes:
- `en` - English (default)
- `ja` - Japanese
- `zh` - Chinese
- `es` - Spanish
- `fr` - French
- `de` - German
- `ko` - Korean

## Testing
```bash
# Verify default is English
whisper-srt --help | grep language

# Test with explicit language
whisper-srt input.mp3 --language ja
```

## Dependencies
- None (can be implemented independently)
