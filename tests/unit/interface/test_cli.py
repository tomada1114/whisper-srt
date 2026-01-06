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

    def test_parser_accepts_no_arguments(self) -> None:
        """Parser should accept no arguments (input is optional at parse level)."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args([])

        assert args.input is None
        assert args.init is False

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

    def test_parser_language_default_is_none(self) -> None:
        """Parser should default language to None (loaded from config at runtime)."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3"])

        assert args.language is None

    def test_parser_accepts_verbose_flag(self) -> None:
        """Parser should accept -v/--verbose flag."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3", "-v"])

        assert args.verbose is True

    def test_parser_accepts_vocabulary_option(self) -> None:
        """Parser should accept --vocabulary option."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3", "--vocabulary", "/path/to/vocab.txt"])

        assert args.vocabulary == Path("/path/to/vocab.txt")

    def test_parser_accepts_no_vocabulary_flag(self) -> None:
        """Parser should accept --no-vocabulary flag."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3", "--no-vocabulary"])

        assert args.no_vocabulary is True

    def test_parser_vocabulary_and_no_vocabulary_are_mutually_exclusive(self) -> None:
        """Parser should reject --vocabulary and --no-vocabulary together."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(
                ["input.mp3", "--vocabulary", "/path/to/vocab.txt", "--no-vocabulary"]
            )


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

    def test_main_passes_vocabulary_to_client(self) -> None:
        """main should pass custom vocabulary file to client."""
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
                        vocab_path = Path(tmpdir) / "vocab.txt"
                        vocab_path.write_text("term1\nterm2\nterm3")

                        result = main(
                            [str(audio_path), "--vocabulary", str(vocab_path)]
                        )

                        assert result == 0
                        call_kwargs = (
                            mock_openai.audio.transcriptions.create.call_args.kwargs
                        )
                        assert call_kwargs["prompt"] == "term1, term2, term3"

    def test_main_no_vocabulary_passes_empty_prompt(self) -> None:
        """main should pass empty vocabulary when --no-vocabulary is used."""
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

                        result = main([str(audio_path), "--no-vocabulary"])

                        assert result == 0
                        call_kwargs = (
                            mock_openai.audio.transcriptions.create.call_args.kwargs
                        )
                        assert call_kwargs["prompt"] == ""

    def test_main_returns_1_for_nonexistent_vocabulary_file(self) -> None:
        """main should return 1 if vocabulary file doesn't exist."""
        from transcribe.interface.cli import main

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "input.mp3"
            audio_path.touch()

            result = main(
                [str(audio_path), "--vocabulary", "/nonexistent/vocab.txt"]
            )

            assert result == 1

    def test_main_loads_default_vocabulary_when_exists(self) -> None:
        """main should load default vocabulary file when it exists."""
        mock_openai = MagicMock()
        mock_openai.audio.transcriptions.create.return_value = SAMPLE_SRT

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("transcribe.infrastructure.openai_client.load_dotenv"):
                with patch(
                    "transcribe.infrastructure.openai_client.OpenAI",
                    return_value=mock_openai,
                ):
                    with tempfile.TemporaryDirectory() as tmpdir:
                        audio_path = Path(tmpdir) / "input.mp3"
                        audio_path.touch()
                        vocab_file = Path(tmpdir) / "vocabulary.txt"
                        vocab_file.write_text("default1\ndefault2")

                        with patch(
                            "transcribe.interface.cli.load_default_vocabulary",
                            return_value=("default1", "default2"),
                        ):
                            from transcribe.interface.cli import main

                            result = main([str(audio_path)])

                            assert result == 0
                            call_kwargs = (
                                mock_openai.audio.transcriptions.create.call_args.kwargs
                            )
                            assert call_kwargs["prompt"] == "default1, default2"


@pytest.mark.unit
class TestCLIInit:
    """Tests for --init option."""

    def test_parser_accepts_init_flag(self) -> None:
        """Parser should accept --init flag."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["--init"])

        assert args.init is True
        assert args.input is None

    def test_init_creates_vocabulary_file(self, tmp_path: Path) -> None:
        """--init should create vocabulary file and return 0."""
        vocab_path = tmp_path / "vocabulary.txt"
        lang_path = tmp_path / "language.txt"

        with (
            patch(
                "transcribe.domain.vocabulary_loader.DEFAULT_VOCABULARY_PATH",
                vocab_path,
            ),
            patch(
                "transcribe.interface.cli.prompt_language_selection", return_value="en"
            ),
            patch(
                "transcribe.domain.config_loader.DEFAULT_CONFIG_DIR", tmp_path
            ),
            patch(
                "transcribe.domain.config_loader.DEFAULT_LANGUAGE_PATH", lang_path
            ),
        ):
            from transcribe.interface.cli import main

            result = main(["--init"])

        assert result == 0
        assert vocab_path.exists()
        content = vocab_path.read_text()
        assert "Claude Code" in content
        assert "OpenAI" in content
        assert "Codex" in content

    def test_init_skips_existing_file(self, tmp_path: Path) -> None:
        """--init should skip if file already exists and return 0."""
        vocab_path = tmp_path / "vocabulary.txt"
        vocab_path.write_text("existing content")
        lang_path = tmp_path / "language.txt"

        with (
            patch(
                "transcribe.domain.vocabulary_loader.DEFAULT_VOCABULARY_PATH",
                vocab_path,
            ),
            patch(
                "transcribe.interface.cli.prompt_language_selection", return_value="en"
            ),
            patch(
                "transcribe.domain.config_loader.DEFAULT_CONFIG_DIR", tmp_path
            ),
            patch(
                "transcribe.domain.config_loader.DEFAULT_LANGUAGE_PATH", lang_path
            ),
        ):
            from transcribe.interface.cli import main

            result = main(["--init"])

        assert result == 0
        assert vocab_path.read_text() == "existing content"

    def test_init_saves_selected_language(self, tmp_path: Path) -> None:
        """--init should save selected language to config file."""
        vocab_path = tmp_path / "vocabulary.txt"
        lang_path = tmp_path / "language.txt"

        with (
            patch(
                "transcribe.domain.vocabulary_loader.DEFAULT_VOCABULARY_PATH",
                vocab_path,
            ),
            patch(
                "transcribe.interface.cli.prompt_language_selection", return_value="ja"
            ),
            patch(
                "transcribe.domain.config_loader.DEFAULT_CONFIG_DIR", tmp_path
            ),
            patch(
                "transcribe.domain.config_loader.DEFAULT_LANGUAGE_PATH", lang_path
            ),
        ):
            from transcribe.interface.cli import main

            result = main(["--init"])

        assert result == 0
        assert lang_path.exists()
        assert lang_path.read_text() == "ja\n"

    def test_main_requires_input_when_not_init(self) -> None:
        """main should require input file when --init is not used."""
        from transcribe.interface.cli import main

        with pytest.raises(SystemExit) as exc_info:
            main([])

        assert exc_info.value.code == 2  # argparse error exit code
