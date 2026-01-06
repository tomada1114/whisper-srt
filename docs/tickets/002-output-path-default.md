# Ticket #2: Change Default Output Path

## Overview
Change the default output filename from `{input}_transcribed.srt` to `{input}.srt` (same name as input, different extension only).

## Acceptance Criteria
- [ ] Default output: `input.mp3` → `input.srt` (not `input_transcribed.srt`)
- [ ] Output file is saved in the same directory as input file
- [ ] `-o` / `--output` option still works for custom output path
- [ ] Help text and examples updated
- [ ] Tests updated for new default behavior

## Implementation

### Files to Modify
- `src/transcribe/interface/cli.py`
  ```python
  # Before
  output_path = input_path.parent / f"{input_path.stem}_transcribed.srt"

  # After
  output_path = input_path.with_suffix(".srt")
  ```

### Help Text Update
```
Examples:
  whisper-srt input.mp3                   # Output: input.srt
  whisper-srt input.mp3 -o custom.srt     # Output: custom.srt
```

## Testing
```bash
# Verify default output name
whisper-srt test.mp3
ls test.srt  # Should exist

# Verify custom output still works
whisper-srt test.mp3 -o custom.srt
ls custom.srt  # Should exist
```

## Dependencies
- None (can be implemented independently)
