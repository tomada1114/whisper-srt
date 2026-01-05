"""Tests for WhisperTranscriptionClient.

Note: These tests mock the stable_whisper module to avoid:
1. Loading large Whisper models (several GB)
2. Long processing times (minutes per audio file)
3. Requiring actual audio files
"""

import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


def _create_mock_stable_whisper(segment_count: int = 3) -> MagicMock:
    """Create a mock stable_whisper module."""
    mock_module = MagicMock()
    mock_model = MagicMock()
    mock_result = MagicMock()
    mock_result.split_by_length.return_value = mock_result
    mock_result.__iter__ = MagicMock(return_value=iter([MagicMock() for _ in range(segment_count)]))
    mock_model.transcribe.return_value = mock_result
    mock_module.load_model.return_value = mock_model
    return mock_module


@pytest.mark.unit
class TestWhisperTranscriptionClient:
    """Tests for WhisperTranscriptionClient class."""

    def test_transcribe_creates_srt_file(self) -> None:
        """transcribe should create an SRT file at output_path."""
        # Arrange
        mock_whisper = _create_mock_stable_whisper()
        mock_result = mock_whisper.load_model.return_value.transcribe.return_value

        with patch.dict(sys.modules, {"stable_whisper": mock_whisper}):
            from transcribe.infrastructure.whisper_client import (
                WhisperTranscriptionClient,
            )

            client = WhisperTranscriptionClient()

            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = Path(tmpdir) / "source.mp3"
                audio_path.touch()
                output_path = Path(tmpdir) / "subtitle.srt"

                # Act
                client.transcribe(audio_path, output_path)

                # Assert
                mock_result.to_srt_vtt.assert_called_once()

    def test_transcribe_raises_on_nonexistent_audio(self) -> None:
        """transcribe should raise FileNotFoundError if audio file doesn't exist."""
        # Arrange
        mock_whisper = _create_mock_stable_whisper()

        with patch.dict(sys.modules, {"stable_whisper": mock_whisper}):
            from transcribe.infrastructure.whisper_client import (
                WhisperTranscriptionClient,
            )

            client = WhisperTranscriptionClient()

            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = Path(tmpdir) / "nonexistent.mp3"
                output_path = Path(tmpdir) / "subtitle.srt"

                # Act & Assert
                with pytest.raises(FileNotFoundError):
                    client.transcribe(audio_path, output_path)

    def test_transcribe_returns_segment_count(self) -> None:
        """transcribe should return segment count."""
        # Arrange
        mock_whisper = _create_mock_stable_whisper(segment_count=5)

        with patch.dict(sys.modules, {"stable_whisper": mock_whisper}):
            from transcribe.infrastructure.whisper_client import (
                WhisperTranscriptionClient,
            )

            client = WhisperTranscriptionClient()

            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = Path(tmpdir) / "source.mp3"
                audio_path.touch()
                output_path = Path(tmpdir) / "subtitle.srt"

                # Act
                count = client.transcribe(audio_path, output_path)

                # Assert
                assert count == 5

    def test_transcribe_uses_correct_parameters(self) -> None:
        """transcribe should use correct Whisper parameters."""
        # Arrange
        mock_whisper = _create_mock_stable_whisper()
        mock_model = mock_whisper.load_model.return_value

        with patch.dict(sys.modules, {"stable_whisper": mock_whisper}):
            from transcribe.infrastructure.whisper_client import (
                WhisperTranscriptionClient,
            )

            client = WhisperTranscriptionClient()

            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = Path(tmpdir) / "source.mp3"
                audio_path.touch()
                output_path = Path(tmpdir) / "subtitle.srt"

                # Act
                client.transcribe(audio_path, output_path)

                # Assert
                mock_whisper.load_model.assert_called_with("large", device="cpu")
                call_kwargs = mock_model.transcribe.call_args.kwargs
                assert call_kwargs["language"] == "Japanese"
                assert call_kwargs["fp16"] is False
                assert call_kwargs["regroup"] is True

    def test_transcribe_raises_runtime_error_on_model_failure(self) -> None:
        """transcribe should raise RuntimeError if model loading fails."""
        # Arrange
        mock_whisper = MagicMock()
        mock_whisper.load_model.side_effect = Exception("Model loading failed")

        with patch.dict(sys.modules, {"stable_whisper": mock_whisper}):
            from transcribe.infrastructure.whisper_client import (
                WhisperTranscriptionClient,
            )

            client = WhisperTranscriptionClient()

            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = Path(tmpdir) / "source.mp3"
                audio_path.touch()
                output_path = Path(tmpdir) / "subtitle.srt"

                # Act & Assert
                with pytest.raises(RuntimeError, match="Model loading failed"):
                    client.transcribe(audio_path, output_path)

    def test_transcribe_includes_custom_vocabulary(self) -> None:
        """transcribe should include custom vocabulary in prompt."""
        # Arrange
        mock_whisper = _create_mock_stable_whisper()
        mock_model = mock_whisper.load_model.return_value

        with patch.dict(sys.modules, {"stable_whisper": mock_whisper}):
            from transcribe.infrastructure.whisper_client import (
                WhisperTranscriptionClient,
            )

            client = WhisperTranscriptionClient()

            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = Path(tmpdir) / "source.mp3"
                audio_path.touch()
                output_path = Path(tmpdir) / "subtitle.srt"

                # Act
                client.transcribe(audio_path, output_path)

                # Assert
                call_kwargs = mock_model.transcribe.call_args.kwargs
                # Check that vocabulary prompt contains key terms
                assert "Claude" in call_kwargs["initial_prompt"]
                assert "MCP" in call_kwargs["initial_prompt"]

    def test_transcribe_with_custom_model_and_language(self) -> None:
        """transcribe should use custom model and language settings."""
        # Arrange
        mock_whisper = _create_mock_stable_whisper()
        mock_model = mock_whisper.load_model.return_value

        with patch.dict(sys.modules, {"stable_whisper": mock_whisper}):
            from transcribe.infrastructure.whisper_client import (
                WhisperTranscriptionClient,
            )

            client = WhisperTranscriptionClient(
                model_size="medium",
                language="en",
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = Path(tmpdir) / "source.mp3"
                audio_path.touch()
                output_path = Path(tmpdir) / "subtitle.srt"

                # Act
                client.transcribe(audio_path, output_path)

                # Assert
                mock_whisper.load_model.assert_called_with("medium", device="cpu")
                call_kwargs = mock_model.transcribe.call_args.kwargs
                assert call_kwargs["language"] == "en"
