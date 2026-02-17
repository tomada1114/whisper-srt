"""Supported audio formats for transcription.

Defines the set of audio file extensions supported by the OpenAI Whisper API.
This serves as the single source of truth for format validation across the application.
"""

from __future__ import annotations

__all__ = ["SUPPORTED_AUDIO_EXTENSIONS"]

# Audio formats supported by OpenAI Whisper API (whisper-1)
# Reference: https://platform.openai.com/docs/api-reference/audio/createTranscription
SUPPORTED_AUDIO_EXTENSIONS: frozenset[str] = frozenset(
    {".flac", ".m4a", ".mp3", ".mp4", ".mpeg", ".mpga", ".oga", ".ogg", ".wav", ".webm"}
)
