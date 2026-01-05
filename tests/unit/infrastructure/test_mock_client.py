"""Tests for MockTranscriptionClient."""

import tempfile
from pathlib import Path

import pytest


@pytest.mark.unit
class TestMockTranscriptionClient:
    """Tests for MockTranscriptionClient class."""

    def test_transcribe_creates_srt_file(self) -> None:
        """transcribe should create an SRT file at output_path."""
        # Arrange
        from transcribe.infrastructure.mock_client import MockTranscriptionClient

        client = MockTranscriptionClient()
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            # Act
            client.transcribe(audio_path, output_path)

            # Assert
            assert output_path.exists()

    def test_transcribe_returns_segment_count(self) -> None:
        """transcribe should return a positive segment count."""
        # Arrange
        from transcribe.infrastructure.mock_client import MockTranscriptionClient

        client = MockTranscriptionClient()
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            # Act
            segment_count = client.transcribe(audio_path, output_path)

            # Assert
            assert isinstance(segment_count, int)
            assert segment_count > 0

    def test_transcribe_creates_valid_srt_content(self) -> None:
        """transcribe should create valid SRT format content."""
        # Arrange
        from transcribe.infrastructure.mock_client import MockTranscriptionClient

        client = MockTranscriptionClient()
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            # Act
            client.transcribe(audio_path, output_path)

            # Assert
            content = output_path.read_text(encoding="utf-8")
            # SRT format: number, timestamp, text, blank line
            assert "1\n" in content
            assert " --> " in content
            assert content.strip()  # Non-empty

    def test_transcribe_raises_on_nonexistent_audio(self) -> None:
        """transcribe should raise FileNotFoundError if audio file doesn't exist."""
        # Arrange
        from transcribe.infrastructure.mock_client import MockTranscriptionClient

        client = MockTranscriptionClient()
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "nonexistent.mp3"
            output_path = Path(tmpdir) / "subtitle.srt"

            # Act & Assert
            with pytest.raises(FileNotFoundError):
                client.transcribe(audio_path, output_path)

    def test_transcribe_creates_parent_directories(self) -> None:
        """transcribe should create parent directories if they don't exist."""
        # Arrange
        from transcribe.infrastructure.mock_client import MockTranscriptionClient

        client = MockTranscriptionClient()
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "nested" / "dir" / "subtitle.srt"

            # Act
            client.transcribe(audio_path, output_path)

            # Assert
            assert output_path.exists()
