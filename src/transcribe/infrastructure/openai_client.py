"""OpenAI Whisper API transcription client.

This module provides a transcription implementation using OpenAI's
Whisper API (whisper-1 model) for cloud-based speech-to-text conversion.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Optional, Tuple

from dotenv import load_dotenv
from openai import OpenAI

from transcribe.domain.vocabulary import DEFAULT_VOCABULARY

logger = logging.getLogger(__name__)


class OpenAITranscriptionClient:
    """Transcription client using OpenAI Whisper API.

    This implementation uses OpenAI's cloud-based Whisper API (whisper-1),
    which directly outputs SRT format without local model loading.

    Configuration:
        - Model: whisper-1 (OpenAI's hosted Whisper)
        - Language: Japanese (default, configurable)
        - API Key: Read from OPENAI_API_KEY environment variable
        - Vocabulary: Custom terms to improve recognition accuracy

    Example:
        >>> from pathlib import Path
        >>> client = OpenAITranscriptionClient()
        >>> count = client.transcribe(
        ...     audio_path=Path("audio/source.mp3"),
        ...     output_path=Path("subtitle.srt"),
        ... )
        >>> print(f"Generated {count} segments")
    """

    _DEFAULT_LANGUAGE = "ja"

    def __init__(
        self,
        language: Optional[str] = None,
        vocabulary: Optional[Tuple[str, ...]] = None,
    ) -> None:
        """Initialize the OpenAI transcription client.

        Loads API key from environment variable OPENAI_API_KEY.
        The .env file is automatically loaded if present.

        Args:
            language: Target language code for transcription (ISO-639-1).
                Default is "ja" for Japanese.
            vocabulary: Custom vocabulary terms to improve recognition.
                Default is built-in AI/MCP technical terms.

        Raises:
            ValueError: If OPENAI_API_KEY environment variable is not set.
        """
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            msg = "OPENAI_API_KEY environment variable is not set"
            raise ValueError(msg)

        self._client = OpenAI(api_key=api_key)
        self._language = language or self._DEFAULT_LANGUAGE
        self._vocabulary = vocabulary or DEFAULT_VOCABULARY

    def _build_prompt(self) -> str:
        """Build prompt string from vocabulary for Whisper API.

        OpenAI Whisper API accepts a prompt parameter to guide transcription.
        This helps with recognition of technical terms, names, and jargon.

        Note: Prompt token limit is 244 tokens. Long vocabularies may be truncated.

        Returns:
            Prompt string containing vocabulary terms.
        """
        vocab_str = ", ".join(self._vocabulary)
        return vocab_str

    def transcribe(
        self,
        audio_path: Path,
        output_path: Path,
    ) -> int:
        """Transcribe audio file to SRT format using OpenAI Whisper API.

        Calls OpenAI's Whisper API with response_format="srt" to get
        SRT-formatted subtitles directly.

        Args:
            audio_path: Path to the input audio file (MP3 format).
            output_path: Path where the SRT file will be saved.

        Returns:
            Number of subtitle segments generated.

        Raises:
            FileNotFoundError: If audio_path does not exist.
            RuntimeError: If API call or transcription fails.
        """
        # Validate audio file exists
        if not audio_path.exists():
            msg = f"Audio file not found: {audio_path}"
            raise FileNotFoundError(msg)

        # Create parent directories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            logger.info("Calling OpenAI Whisper API for %s...", audio_path)

            prompt = self._build_prompt()
            logger.debug("Using prompt with %d vocabulary terms", len(self._vocabulary))

            with open(audio_path, "rb") as audio_file:
                transcript = self._client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="srt",
                    language=self._language,
                    prompt=prompt,
                )

            # Write SRT content to file
            output_path.write_text(transcript, encoding="utf-8")

            # Count segments (SRT segments start with a number on its own line)
            segment_count = len(re.findall(r"^\d+$", transcript, re.MULTILINE))

            logger.info(
                "Transcription complete: %d segments saved to %s",
                segment_count,
                output_path,
            )

            return segment_count

        except FileNotFoundError:
            raise
        except Exception as e:
            msg = f"Transcription failed: {e}"
            logger.exception(msg)
            raise RuntimeError(msg) from e
