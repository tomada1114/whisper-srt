---
name: transcribe-audio
description: >
  Transcribe an audio file to text using the whisper-srt CLI.
  The output .txt file is saved in the same directory as the input audio.
  Use PROACTIVELY when the user provides an absolute path to an audio file
  (mp3, webm, wav, m4a, ogg, flac, mp4, mpeg, mpga, oga) and asks to
  transcribe it, convert it to text, or perform 文字起こし.
  Also use when user says "文字起こしして", "テキスト化して", "書き起こして".
  Argument: absolute path to the audio file.
argument-hint: /absolute/path/to/audio.webm
---

## Transcribe Audio to Text

Transcribe the specified audio file and save the result as `.txt` in the same directory.

### Steps

1. Confirm the audio file exists at the given path.
2. Run transcription from the project root with venv activated:

```bash
cd /Users/masuyama/ghq/github.com/tomada1114/whisper-srt
source venv/bin/activate
python -m transcribe "<absolute_path>" --text
```

3. Report the output path to the user. The output file is `<same_dir>/<stem>.txt`.

### Notes

- Supported formats: mp3, webm, wav, m4a, ogg, flac, mp4, mpeg, mpga, oga
- Default language is Japanese (`ja`). Pass `--language en` if English is needed.
- If `OPENAI_API_KEY` is not set, the command will fail with a clear error.
- Run in background (`run_in_background: true` on Bash tool) since API calls take time.
- After completion, show the output file path and optionally display the transcribed text.
