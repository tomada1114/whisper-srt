"""Tests for CLI module."""

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
class TestCLIParser:
    """Tests for CLI argument parser."""

    def test_parser_requires_input_file(self) -> None:
        """Parser should require input file argument."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_parser_accepts_input_file(self) -> None:
        """Parser should accept input file argument."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3"])

        assert args.input == Path("input.mp3")

    def test_parser_accepts_output_option(self) -> None:
        """Parser should accept -o/--output option."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3", "-o", "output.srt"])

        assert args.output == Path("output.srt")

    def test_parser_accepts_language_option(self) -> None:
        """Parser should accept --language option."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3", "--language", "en"])

        assert args.language == "en"

    def test_parser_language_default_is_en(self) -> None:
        """Parser should default to en (English) language."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3"])

        assert args.language == "en"

    def test_parser_accepts_verbose_flag(self) -> None:
        """Parser should accept -v/--verbose flag."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3", "-v"])

        assert args.verbose is True


@pytest.mark.unit
class TestCLIMain:
    """Tests for CLI main function."""

    def test_main_returns_1_for_nonexistent_input(self) -> None:
        """main should return 1 if input file doesn't exist."""
        from transcribe.interface.cli import main

        result = main(["nonexistent.mp3"])

        assert result == 1

    def test_main_returns_0_on_success(self) -> None:
        """main should return 0 on successful transcription."""
        mock_openai = MagicMock()
        mock_openai.audio.transcriptions.create.return_value = SAMPLE_SRT

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    from transcribe.interface.cli import main

                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "input.mp3"
                        audio_path.touch()

                        result = main([str(audio_path)])

                        assert result == 0

    def test_main_creates_default_output_file(self) -> None:
        """main should create output file with default name."""
        mock_openai = MagicMock()
        mock_openai.audio.transcriptions.create.return_value = SAMPLE_SRT

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    from transcribe.interface.cli import main

                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "input.mp3"
                        audio_path.touch()

                        result = main([str(audio_path)])

                        assert result == 0
                        expected_output = Path(tmpdir) / "input.srt"
                        assert expected_output.exists()

    def test_main_returns_1_when_api_key_missing(self) -> None:
        """main should return 1 if OPENAI_API_KEY is not set."""
        with patch.dict("os.environ", {}, clear=True):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                from transcribe.interface.cli import main

                with tempfile.TemporaryDirectory() as tmpdir:
                    audio_path = Path(tmpdir) / "input.mp3"
                    audio_path.touch()

                    result = main([str(audio_path)])

                    assert result == 1

    def test_main_uses_specified_output_path(self) -> None:
        """main should use specified output path."""
        mock_openai = MagicMock()
        mock_openai.audio.transcriptions.create.return_value = SAMPLE_SRT

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    from transcribe.interface.cli import main

                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "input.mp3"
                        audio_path.touch()
                        output_path = Path(tmpdir) / "custom_output.srt"

                        result = main([str(audio_path), "-o", str(output_path)])

                        assert result == 0
                        assert output_path.exists()

    def test_main_passes_language_to_client(self) -> None:
        """main should pass language option to client."""
        mock_openai = MagicMock()
        mock_openai.audio.transcriptions.create.return_value = SAMPLE_SRT

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    from transcribe.interface.cli import main

                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "input.mp3"
                        audio_path.touch()

                        result = main([str(audio_path), "--language", "en"])

                        assert result == 0
                        call_kwargs = mock_openai.audio.transcriptions.create.call_args.kwargs
                        assert call_kwargs["language"] == "en"
