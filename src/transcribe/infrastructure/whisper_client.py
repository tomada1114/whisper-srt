"""Whisper transcription client using stable-ts.

This module provides a transcription implementation using stable-ts
(stable-whisper) for accurate speech-to-text with timing information.

Note: stable_whisper is imported lazily to allow testing without
the dependency installed.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Tuple

from transcribe.domain.vocabulary import DEFAULT_VOCABULARY

logger = logging.getLogger(__name__)


class WhisperTranscriptionClient:
    """Transcription client using stable-ts (stable-whisper).

    This implementation uses stable-ts, which provides enhanced timing
    accuracy compared to vanilla Whisper. It generates SRT files with
    properly aligned timestamps.

    Configuration:
        - Model: large (default, configurable)
        - Language: Japanese (default, configurable)
        - Max characters per line: 24 (optimized for readability)
        - Custom vocabulary: AI-driven development terms

    Example:
        >>> from pathlib import Path
        >>> client = WhisperTranscriptionClient()
        >>> count = client.transcribe(
        ...     audio_path=Path("audio/source.mp3"),
        ...     output_path=Path("subtitle.srt"),
        ... )
        >>> print(f"Generated {count} segments")
    """

    # Default configuration
    _DEFAULT_MODEL_SIZE = "large"
    _DEFAULT_LANGUAGE = "Japanese"
    _MAX_CHARS = 24

    def __init__(
        self,
        model_size: Optional[str] = None,
        language: Optional[str] = None,
        vocabulary: Optional[Tuple[str, ...]] = None,
    ) -> None:
        """Initialize the transcription client.

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large).
                Default is "large" for best accuracy.
            language: Target language for transcription. Default is "Japanese".
            vocabulary: Custom vocabulary terms to improve recognition.
                Default is built-in AI/MCP technical terms.
        """
        self._model_size = model_size or self._DEFAULT_MODEL_SIZE
        self._language = language or self._DEFAULT_LANGUAGE
        self._vocabulary = vocabulary or DEFAULT_VOCABULARY

    def transcribe(
        self,
        audio_path: Path,
        output_path: Path,
    ) -> int:
        """Transcribe audio file to SRT format.

        Loads the Whisper model, performs transcription with custom
        vocabulary, and saves the result as an SRT file.

        Args:
            audio_path: Path to the input audio file (MP3 format).
            output_path: Path where the SRT file will be saved.

        Returns:
            Number of subtitle segments generated.

        Raises:
            FileNotFoundError: If audio_path does not exist.
            RuntimeError: If model loading or transcription fails.
        """
        # Validate audio file exists
        if not audio_path.exists():
            msg = f"Audio file not found: {audio_path}"
            raise FileNotFoundError(msg)

        # Create parent directories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Lazy import to allow testing without dependency
            import stable_whisper  # noqa: PLC0415

            # Load model (CPU環境では明示的にdeviceを指定)
            logger.info("Loading Whisper model '%s'...", self._model_size)
            model = stable_whisper.load_model(self._model_size, device="cpu")
            logger.info("Model loaded successfully")

            # Build vocabulary prompt
            vocab_str = ", ".join(self._vocabulary)
            prompt_text = f"この動画では、以下の技術用語やツールについて話しています: {vocab_str}。"

            # Transcribe (CPU環境では fp16=False を明示的に指定)
            logger.info("Starting transcription of %s...", audio_path)
            result = model.transcribe(
                str(audio_path),
                language=self._language,
                initial_prompt=prompt_text,
                fp16=False,
                regroup=True,
                condition_on_previous_text=False,
                no_speech_threshold=0.6,
                compression_ratio_threshold=2.4,
            )

            # Split by max characters and save as SRT
            logger.info("Splitting subtitles (max %d chars per line)...", self._MAX_CHARS)
            split_result = result.split_by_length(max_chars=self._MAX_CHARS)
            split_result.to_srt_vtt(str(output_path), word_level=False)

            # Count segments
            segment_count = len(list(split_result))
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
