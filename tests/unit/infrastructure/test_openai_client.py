"""Tests for OpenAITranscriptionClient.

Note: These tests mock the OpenAI API to avoid:
1. Making actual API calls
2. Requiring valid API keys
3. Incurring API costs
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Sample SRT content for mocking
SAMPLE_SRT = """1
00:00:00,000 --> 00:00:03,500
こんにちは、今日はテストです。

2
00:00:03,500 --> 00:00:07,000
これはサンプルの字幕です。

3
00:00:07,000 --> 00:00:11,500
テストが正常に動作しています。
"""


@pytest.mark.unit
class TestOpenAITranscriptionClientInit:
    """Tests for OpenAITranscriptionClient initialization."""

    def test_init_raises_without_api_key(self) -> None:
        """__init__ should raise ValueError if OPENAI_API_KEY is not set."""
        with patch.dict("os.environ", {}, clear=True):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                from transcribe.infrastructure.openai_client import (
                    OpenAITranscriptionClient,
                )

                with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                    OpenAITranscriptionClient()

    def test_init_succeeds_with_api_key(self) -> None:
        """__init__ should succeed when OPENAI_API_KEY is set."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch("transcribe.infrastructure.openai_client.OpenAI"):
                    from transcribe.infrastructure.openai_client import (
                        OpenAITranscriptionClient,
                    )

                    client = OpenAITranscriptionClient()
                    assert client._language == "ja"

    def test_init_with_custom_language(self) -> None:
        """__init__ should accept custom language parameter."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch("transcribe.infrastructure.openai_client.OpenAI"):
                    from transcribe.infrastructure.openai_client import (
                        OpenAITranscriptionClient,
                    )

                    client = OpenAITranscriptionClient(language="en")
                    assert client._language == "en"

    def test_init_uses_default_vocabulary(self) -> None:
        """__init__ should use DEFAULT_VOCABULARY when not specified."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch("transcribe.infrastructure.openai_client.OpenAI"):
                    from transcribe.domain.vocabulary import DEFAULT_VOCABULARY
                    from transcribe.infrastructure.openai_client import (
                        OpenAITranscriptionClient,
                    )

                    client = OpenAITranscriptionClient()
                    assert client._vocabulary == DEFAULT_VOCABULARY


@pytest.mark.unit
class TestOpenAITranscriptionClientTranscribe:
    """Tests for OpenAITranscriptionClient.transcribe method."""

    def test_transcribe_creates_srt_file(self) -> None:
        """transcribe should create an SRT file at output_path."""
        mock_openai = MagicMock()
        mock_openai.audio.transcriptions.create.return_value = SAMPLE_SRT

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    from transcribe.infrastructure.openai_client import (
                        OpenAITranscriptionClient,
                    )

                    client = OpenAITranscriptionClient()

                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "source.mp3"
                        audio_path.touch()
                        output_path = Path(tmpdir) / "subtitle.srt"

                        client.transcribe(audio_path, output_path)

                        assert output_path.exists()
                        content = output_path.read_text(encoding="utf-8")
                        assert "こんにちは" in content

    def test_transcribe_raises_on_nonexistent_audio(self) -> None:
        """transcribe should raise FileNotFoundError if audio file doesn't exist."""
        mock_openai = MagicMock()

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    from transcribe.infrastructure.openai_client import (
                        OpenAITranscriptionClient,
                    )

                    client = OpenAITranscriptionClient()

                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "nonexistent.mp3"
                        output_path = Path(tmpdir) / "subtitle.srt"

                        with pytest.raises(FileNotFoundError):
                            client.transcribe(audio_path, output_path)

    def test_transcribe_returns_segment_count(self) -> None:
        """transcribe should return correct segment count."""
        mock_openai = MagicMock()
        mock_openai.audio.transcriptions.create.return_value = SAMPLE_SRT

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    from transcribe.infrastructure.openai_client import (
                        OpenAITranscriptionClient,
                    )

                    client = OpenAITranscriptionClient()

                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "source.mp3"
                        audio_path.touch()
                        output_path = Path(tmpdir) / "subtitle.srt"

                        count = client.transcribe(audio_path, output_path)

                        assert count == 3

    def test_transcribe_calls_api_with_correct_parameters(self) -> None:
        """transcribe should call OpenAI API with correct parameters including prompt."""
        mock_openai = MagicMock()
        mock_openai.audio.transcriptions.create.return_value = SAMPLE_SRT

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    from transcribe.infrastructure.openai_client import (
                        OpenAITranscriptionClient,
                    )

                    client = OpenAITranscriptionClient(language="ja")

                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "source.mp3"
                        audio_path.touch()
                        output_path = Path(tmpdir) / "subtitle.srt"

                        client.transcribe(audio_path, output_path)

                        call_kwargs = mock_openai.audio.transcriptions.create.call_args.kwargs
                        assert call_kwargs["model"] == "whisper-1"
                        assert call_kwargs["response_format"] == "srt"
                        assert call_kwargs["language"] == "ja"
                        # Verify prompt contains vocabulary terms
                        assert "prompt" in call_kwargs
                        assert "Claude" in call_kwargs["prompt"]

    def test_transcribe_raises_runtime_error_on_api_failure(self) -> None:
        """transcribe should raise RuntimeError if API call fails."""
        mock_openai = MagicMock()
        mock_openai.audio.transcriptions.create.side_effect = Exception("API error")

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    from transcribe.infrastructure.openai_client import (
                        OpenAITranscriptionClient,
                    )

                    client = OpenAITranscriptionClient()

                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "source.mp3"
                        audio_path.touch()
                        output_path = Path(tmpdir) / "subtitle.srt"

                        with pytest.raises(RuntimeError, match="API error"):
                            client.transcribe(audio_path, output_path)

    def test_transcribe_creates_parent_directories(self) -> None:
        """transcribe should create parent directories for output path."""
        mock_openai = MagicMock()
        mock_openai.audio.transcriptions.create.return_value = SAMPLE_SRT

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    from transcribe.infrastructure.openai_client import (
                        OpenAITranscriptionClient,
                    )

                    client = OpenAITranscriptionClient()

                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "source.mp3"
                        audio_path.touch()
                        output_path = Path(tmpdir) / "nested" / "dir" / "subtitle.srt"

                        client.transcribe(audio_path, output_path)

                        assert output_path.exists()

    def test_transcribe_handles_empty_srt(self) -> None:
        """transcribe should handle empty SRT response."""
        mock_openai = MagicMock()
        mock_openai.audio.transcriptions.create.return_value = ""

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    from transcribe.infrastructure.openai_client import (
                        OpenAITranscriptionClient,
                    )

                    client = OpenAITranscriptionClient()

                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "source.mp3"
                        audio_path.touch()
                        output_path = Path(tmpdir) / "subtitle.srt"

                        count = client.transcribe(audio_path, output_path)

                        assert count == 0
                        assert output_path.exists()
