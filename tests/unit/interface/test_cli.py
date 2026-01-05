"""Tests for CLI module."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


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

    def test_parser_accepts_model_option(self) -> None:
        """Parser should accept --model option."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3", "--model", "medium"])

        assert args.model == "medium"

    def test_parser_model_default_is_large(self) -> None:
        """Parser should default to large model."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3"])

        assert args.model == "large"

    def test_parser_accepts_language_option(self) -> None:
        """Parser should accept --language option."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3", "--language", "en"])

        assert args.language == "en"

    def test_parser_language_default_is_japanese(self) -> None:
        """Parser should default to Japanese language."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3"])

        assert args.language == "Japanese"

    def test_parser_accepts_vocabulary_option(self) -> None:
        """Parser should accept --vocabulary option."""
        from transcribe.interface.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["input.mp3", "--vocabulary", "vocab.txt"])

        assert args.vocabulary == Path("vocab.txt")

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
        # Arrange
        mock_whisper = MagicMock()
        mock_model = MagicMock()
        mock_result = MagicMock()
        mock_result.split_by_length.return_value = mock_result
        mock_result.__iter__ = MagicMock(return_value=iter([MagicMock() for _ in range(3)]))
        mock_model.transcribe.return_value = mock_result
        mock_whisper.load_model.return_value = mock_model

        with patch.dict(sys.modules, {"stable_whisper": mock_whisper}):
            from transcribe.interface.cli import main

            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = Path(tmpdir) / "input.mp3"
                audio_path.touch()

                # Act
                result = main([str(audio_path)])

                # Assert
                assert result == 0

    def test_main_creates_default_output_file(self) -> None:
        """main should create output file with default name."""
        # Arrange
        mock_whisper = MagicMock()
        mock_model = MagicMock()
        mock_result = MagicMock()
        mock_result.split_by_length.return_value = mock_result
        mock_result.__iter__ = MagicMock(return_value=iter([MagicMock() for _ in range(3)]))
        mock_model.transcribe.return_value = mock_result
        mock_whisper.load_model.return_value = mock_model

        with patch.dict(sys.modules, {"stable_whisper": mock_whisper}):
            from transcribe.interface.cli import main

            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = Path(tmpdir) / "input.mp3"
                audio_path.touch()

                # Act
                result = main([str(audio_path)])

                # Assert
                assert result == 0
                # Verify to_srt_vtt was called with default output path
                expected_output = str(Path(tmpdir) / "input_transcribed.srt")
                mock_result.to_srt_vtt.assert_called_once_with(expected_output, word_level=False)


@pytest.mark.unit
class TestLoadVocabulary:
    """Tests for load_vocabulary function."""

    def test_load_vocabulary_returns_default_when_none(self) -> None:
        """load_vocabulary should return DEFAULT_VOCABULARY when path is None."""
        from transcribe.domain.vocabulary import DEFAULT_VOCABULARY
        from transcribe.interface.cli import load_vocabulary

        result = load_vocabulary(None)

        assert result == DEFAULT_VOCABULARY

    def test_load_vocabulary_reads_file(self) -> None:
        """load_vocabulary should read terms from file."""
        from transcribe.interface.cli import load_vocabulary

        with tempfile.TemporaryDirectory() as tmpdir:
            vocab_path = Path(tmpdir) / "vocab.txt"
            vocab_path.write_text("term1\nterm2\nterm3\n", encoding="utf-8")

            result = load_vocabulary(vocab_path)

            assert result == ("term1", "term2", "term3")

    def test_load_vocabulary_raises_on_nonexistent_file(self) -> None:
        """load_vocabulary should raise FileNotFoundError if file doesn't exist."""
        from transcribe.interface.cli import load_vocabulary

        with pytest.raises(FileNotFoundError):
            load_vocabulary(Path("nonexistent.txt"))

    def test_load_vocabulary_ignores_empty_lines(self) -> None:
        """load_vocabulary should ignore empty lines."""
        from transcribe.interface.cli import load_vocabulary

        with tempfile.TemporaryDirectory() as tmpdir:
            vocab_path = Path(tmpdir) / "vocab.txt"
            vocab_path.write_text("term1\n\nterm2\n  \nterm3\n", encoding="utf-8")

            result = load_vocabulary(vocab_path)

            assert result == ("term1", "term2", "term3")
