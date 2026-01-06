"""Tests for OpenAITranscriptionClient.

Note: These tests mock the OpenAI API to avoid:
1. Making actual API calls
2. Requiring valid API keys
3. Incurring API costs
"""

import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)

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


@pytest.fixture
def mock_openai_env() -> Generator[MagicMock, None, None]:
    """Fixture to mock environment and OpenAI client."""
    mock_openai = MagicMock()
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        with patch("transcribe.infrastructure.openai_client.load_dotenv"):
            with patch(
                "transcribe.infrastructure.openai_client.OpenAI",
                return_value=mock_openai,
            ):
                yield mock_openai


@pytest.fixture
def mock_openai_env_no_key() -> Generator[None, None, None]:
    """Fixture to mock environment without API key."""
    with patch.dict("os.environ", {}, clear=True):
        with patch("transcribe.infrastructure.openai_client.load_dotenv"):
            yield


@pytest.mark.unit
class TestOpenAITranscriptionClientInit:
    """Tests for OpenAITranscriptionClient initialization."""

    def test_init_raises_without_api_key(self, mock_openai_env_no_key: None) -> None:
        """__init__ should raise ValueError if OPENAI_API_KEY is not set."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            OpenAITranscriptionClient()

    def test_init_succeeds_with_api_key(self, mock_openai_env: MagicMock) -> None:
        """__init__ should succeed when OPENAI_API_KEY is set."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        client = OpenAITranscriptionClient()
        assert client._language == "ja"

    def test_init_with_custom_language(self, mock_openai_env: MagicMock) -> None:
        """__init__ should accept custom language parameter."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        client = OpenAITranscriptionClient(language="en")
        assert client._language == "en"

    def test_init_uses_default_vocabulary(self, mock_openai_env: MagicMock) -> None:
        """__init__ should use DEFAULT_VOCABULARY when not specified."""
        from transcribe.domain.vocabulary import DEFAULT_VOCABULARY
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        client = OpenAITranscriptionClient()
        assert client._vocabulary == DEFAULT_VOCABULARY


@pytest.mark.unit
class TestOpenAITranscriptionClientTranscribe:
    """Tests for OpenAITranscriptionClient.transcribe method."""

    def test_transcribe_creates_srt_file(self, mock_openai_env: MagicMock) -> None:
        """transcribe should create an SRT file at output_path."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        mock_openai_env.audio.transcriptions.create.return_value = SAMPLE_SRT
        client = OpenAITranscriptionClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            client.transcribe(audio_path, output_path)

            assert output_path.exists()
            content = output_path.read_text(encoding="utf-8")
            assert "こんにちは" in content

    def test_transcribe_raises_on_nonexistent_audio(
        self, mock_openai_env: MagicMock
    ) -> None:
        """transcribe should raise FileNotFoundError if audio file doesn't exist."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        client = OpenAITranscriptionClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "nonexistent.mp3"
            output_path = Path(tmpdir) / "subtitle.srt"

            with pytest.raises(FileNotFoundError):
                client.transcribe(audio_path, output_path)

    def test_transcribe_returns_segment_count(
        self, mock_openai_env: MagicMock
    ) -> None:
        """transcribe should return correct segment count."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        mock_openai_env.audio.transcriptions.create.return_value = SAMPLE_SRT
        client = OpenAITranscriptionClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            count = client.transcribe(audio_path, output_path)

            assert count == 3

    def test_transcribe_calls_api_with_correct_parameters(
        self, mock_openai_env: MagicMock
    ) -> None:
        """transcribe should call OpenAI API with correct parameters including prompt."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        mock_openai_env.audio.transcriptions.create.return_value = SAMPLE_SRT
        client = OpenAITranscriptionClient(language="ja")

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            client.transcribe(audio_path, output_path)

            call_kwargs = mock_openai_env.audio.transcriptions.create.call_args.kwargs
            assert call_kwargs["model"] == "whisper-1"
            assert call_kwargs["response_format"] == "srt"
            assert call_kwargs["language"] == "ja"
            # Verify prompt is present (empty by default since DEFAULT_VOCABULARY is empty)
            assert "prompt" in call_kwargs
            assert call_kwargs["prompt"] == ""

    def test_transcribe_raises_runtime_error_on_api_failure(
        self, mock_openai_env: MagicMock
    ) -> None:
        """transcribe should raise RuntimeError if API call fails."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        mock_openai_env.audio.transcriptions.create.side_effect = Exception("API error")
        client = OpenAITranscriptionClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            with pytest.raises(RuntimeError, match="API error"):
                client.transcribe(audio_path, output_path)

    def test_transcribe_creates_parent_directories(
        self, mock_openai_env: MagicMock
    ) -> None:
        """transcribe should create parent directories for output path."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        mock_openai_env.audio.transcriptions.create.return_value = SAMPLE_SRT
        client = OpenAITranscriptionClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "nested" / "dir" / "subtitle.srt"

            client.transcribe(audio_path, output_path)

            assert output_path.exists()

    def test_transcribe_handles_empty_srt(self, mock_openai_env: MagicMock) -> None:
        """transcribe should handle empty SRT response."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        mock_openai_env.audio.transcriptions.create.return_value = ""
        client = OpenAITranscriptionClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            count = client.transcribe(audio_path, output_path)

            assert count == 0
            assert output_path.exists()


@pytest.mark.unit
class TestOpenAITranscriptionClientErrorHandling:
    """Tests for specific OpenAI error type handling."""

    def test_transcribe_handles_authentication_error(
        self, mock_openai_env: MagicMock
    ) -> None:
        """transcribe should provide actionable message for auth errors."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_openai_env.audio.transcriptions.create.side_effect = AuthenticationError(
            "Invalid API key",
            response=mock_response,
            body=None,
        )

        client = OpenAITranscriptionClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            with pytest.raises(RuntimeError, match="authentication"):
                client.transcribe(audio_path, output_path)

    def test_transcribe_handles_rate_limit_error(
        self, mock_openai_env: MagicMock
    ) -> None:
        """transcribe should provide actionable message for rate limits."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_openai_env.audio.transcriptions.create.side_effect = RateLimitError(
            "Rate limit exceeded",
            response=mock_response,
            body=None,
        )

        client = OpenAITranscriptionClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            with pytest.raises(RuntimeError, match="rate limit"):
                client.transcribe(audio_path, output_path)

    def test_transcribe_handles_timeout_error(
        self, mock_openai_env: MagicMock
    ) -> None:
        """transcribe should provide actionable message for timeouts."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        mock_request = MagicMock()
        mock_openai_env.audio.transcriptions.create.side_effect = APITimeoutError(
            request=mock_request,
        )

        client = OpenAITranscriptionClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            with pytest.raises(RuntimeError, match="timed out"):
                client.transcribe(audio_path, output_path)

    def test_transcribe_handles_connection_error(
        self, mock_openai_env: MagicMock
    ) -> None:
        """transcribe should provide actionable message for connection errors."""
        from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

        mock_request = MagicMock()
        mock_openai_env.audio.transcriptions.create.side_effect = APIConnectionError(
            request=mock_request,
        )

        client = OpenAITranscriptionClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "source.mp3"
            audio_path.touch()
            output_path = Path(tmpdir) / "subtitle.srt"

            with pytest.raises(RuntimeError, match="connect"):
                client.transcribe(audio_path, output_path)
