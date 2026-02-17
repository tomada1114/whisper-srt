"""Application layer protocols.

This module defines the Protocol interfaces used by the Application layer.
Infrastructure implementations must conform to these protocols.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Protocol

ResponseFormat = Literal["srt", "text"]

__all__ = ["TranscriptionClientProtocol", "ResponseFormat"]


class TranscriptionClientProtocol(Protocol):
    """Protocol for audio transcription implementations.

    This Protocol defines the contract for Whisper-based or other
    speech-to-text transcription services. It enables the Application
    layer to depend on an abstraction rather than concrete implementations,
    supporting dependency injection and facilitating testing.

    Example:
        >>> from transcribe.infrastructure.openai_client import OpenAITranscriptionClient
        >>> from transcribe.application.protocols import TranscriptionClientProtocol
        >>> client: TranscriptionClientProtocol = OpenAITranscriptionClient()
        >>> segment_count = client.transcribe(
        ...     audio_path=Path("audio/source.mp3"),
        ...     output_path=Path("subtitle.srt"),
        ... )
        >>> isinstance(segment_count, int)
        True
    """

    def transcribe(
        self,
        audio_path: Path,
        output_path: Path,
        response_format: ResponseFormat = "srt",
    ) -> int:
        """Transcribe audio file to specified format.

        Converts an audio file to SRT subtitle or plain text format
        using speech-to-text transcription.

        Args:
            audio_path: Path to the input audio file (mp3, webm, wav, m4a, etc.).
                Must be a valid Path object pointing to an existing file.
            output_path: Path where the output file will be saved.
                Parent directory must exist.
            response_format: Output format - "srt" for subtitles with timestamps,
                "text" for plain text. Default is "srt".

        Returns:
            Number of subtitle segments generated (for SRT format),
            or 0 for text format.

        Raises:
            FileNotFoundError: If audio_path does not exist.
            RuntimeError: If transcription fails due to API errors,
                network issues, or other unexpected conditions.

        Preconditions:
            - audio_path exists and is a valid audio file
            - output_path parent directory exists
            - Valid API credentials are configured (e.g., OPENAI_API_KEY)

        Postconditions:
            - Output file is created at output_path
            - For SRT: file contains valid subtitle segments with timestamps
            - Returns segment count (SRT) or 0 (text)
        """
        ...
