"""Tests for vocabulary file loader."""

from pathlib import Path
from unittest.mock import patch

import pytest

from transcribe.domain.vocabulary_loader import (
    DEFAULT_VOCABULARY_PATH,
    SAMPLE_VOCABULARY,
    initialize_vocabulary_file,
    load_default_vocabulary,
    load_vocabulary_from_file,
)


@pytest.mark.unit
class TestLoadVocabularyFromFile:
    """Tests for load_vocabulary_from_file function."""

    def test_loads_vocabulary_from_file(self, tmp_path: Path) -> None:
        """Should load vocabulary terms from a text file."""
        # Given: a vocabulary file with terms
        vocab_file = tmp_path / "vocab.txt"
        vocab_file.write_text("word1\nword2\nword3")

        # When: loading vocabulary from the file
        result = load_vocabulary_from_file(vocab_file)

        # Then: all terms are returned as a tuple
        assert result == ("word1", "word2", "word3")

    def test_skips_empty_lines(self, tmp_path: Path) -> None:
        """Should skip empty lines in vocabulary file."""
        # Given: a vocabulary file with empty lines
        vocab_file = tmp_path / "vocab.txt"
        vocab_file.write_text("word1\n\nword2\n\n\nword3")

        # When: loading vocabulary from the file
        result = load_vocabulary_from_file(vocab_file)

        # Then: only non-empty terms are returned
        assert result == ("word1", "word2", "word3")

    def test_skips_comment_lines(self, tmp_path: Path) -> None:
        """Should skip lines starting with # as comments."""
        # Given: a vocabulary file with comments
        vocab_file = tmp_path / "vocab.txt"
        vocab_file.write_text("# This is a comment\nword1\n# Another comment\nword2")

        # When: loading vocabulary from the file
        result = load_vocabulary_from_file(vocab_file)

        # Then: only non-comment terms are returned
        assert result == ("word1", "word2")

    def test_strips_whitespace(self, tmp_path: Path) -> None:
        """Should strip leading and trailing whitespace from terms."""
        # Given: a vocabulary file with whitespace
        vocab_file = tmp_path / "vocab.txt"
        vocab_file.write_text("  word1  \n\tword2\t\n  word3")

        # When: loading vocabulary from the file
        result = load_vocabulary_from_file(vocab_file)

        # Then: whitespace is stripped from terms
        assert result == ("word1", "word2", "word3")

    def test_raises_file_not_found_error(self) -> None:
        """Should raise FileNotFoundError for non-existent file."""
        # Given: a non-existent file path
        nonexistent_path = Path("/nonexistent/vocab.txt")

        # When/Then: loading vocabulary raises FileNotFoundError
        with pytest.raises(FileNotFoundError) as exc_info:
            load_vocabulary_from_file(nonexistent_path)

        assert "Vocabulary file not found" in str(exc_info.value)

    def test_returns_empty_tuple_for_empty_file(self, tmp_path: Path) -> None:
        """Should return empty tuple for empty file."""
        # Given: an empty vocabulary file
        vocab_file = tmp_path / "vocab.txt"
        vocab_file.write_text("")

        # When: loading vocabulary from the file
        result = load_vocabulary_from_file(vocab_file)

        # Then: empty tuple is returned
        assert result == ()

    def test_returns_empty_tuple_for_comments_only_file(self, tmp_path: Path) -> None:
        """Should return empty tuple for file with only comments."""
        # Given: a vocabulary file with only comments
        vocab_file = tmp_path / "vocab.txt"
        vocab_file.write_text("# Comment 1\n# Comment 2\n")

        # When: loading vocabulary from the file
        result = load_vocabulary_from_file(vocab_file)

        # Then: empty tuple is returned
        assert result == ()

    def test_preserves_phrases_with_spaces(self, tmp_path: Path) -> None:
        """Should preserve multi-word phrases."""
        # Given: a vocabulary file with phrases
        vocab_file = tmp_path / "vocab.txt"
        vocab_file.write_text("Like and Share\nSubscribe Now\nSingle")

        # When: loading vocabulary from the file
        result = load_vocabulary_from_file(vocab_file)

        # Then: phrases are preserved intact
        assert result == ("Like and Share", "Subscribe Now", "Single")


@pytest.mark.unit
class TestLoadDefaultVocabulary:
    """Tests for load_default_vocabulary function."""

    def test_returns_empty_when_default_file_not_exists(self) -> None:
        """Should return empty tuple when default vocabulary file doesn't exist."""
        # Given: default vocabulary path that doesn't exist
        with patch.object(Path, "exists", return_value=False):
            # When: loading default vocabulary
            result = load_default_vocabulary()

        # Then: empty tuple is returned
        assert result == ()

    def test_loads_vocabulary_when_default_file_exists(self, tmp_path: Path) -> None:
        """Should load vocabulary from default path when file exists."""
        # Given: a vocabulary file at the default path
        vocab_file = tmp_path / "vocabulary.txt"
        vocab_file.write_text("term1\nterm2")

        with patch(
            "transcribe.domain.vocabulary_loader.DEFAULT_VOCABULARY_PATH", vocab_file
        ):
            # When: loading default vocabulary
            result = load_default_vocabulary()

        # Then: vocabulary is loaded from the file
        assert result == ("term1", "term2")

    def test_default_vocabulary_path_is_correct(self) -> None:
        """Should have correct default vocabulary path."""
        # Then: default path is ~/.config/whisper-srt/vocabulary.txt
        expected = Path.home() / ".config" / "whisper-srt" / "vocabulary.txt"
        assert DEFAULT_VOCABULARY_PATH == expected


@pytest.mark.unit
class TestInitializeVocabularyFile:
    """Tests for initialize_vocabulary_file function."""

    def test_creates_vocabulary_file_when_not_exists(self, tmp_path: Path) -> None:
        """Should create vocabulary file with sample content when it doesn't exist."""
        # Given: a non-existent vocabulary path
        vocab_path = tmp_path / ".config" / "whisper-srt" / "vocabulary.txt"

        with patch(
            "transcribe.domain.vocabulary_loader.DEFAULT_VOCABULARY_PATH", vocab_path
        ):
            # When: initializing vocabulary file
            created, message = initialize_vocabulary_file()

        # Then: file is created with sample content
        assert created is True
        assert str(vocab_path) in message
        assert vocab_path.exists()
        content = vocab_path.read_text()
        assert "Claude Code" in content
        assert "OpenAI" in content
        assert "Codex" in content

    def test_creates_parent_directory_if_needed(self, tmp_path: Path) -> None:
        """Should create parent directory if it doesn't exist."""
        # Given: a path with non-existent parent directories
        vocab_path = tmp_path / "deep" / "nested" / "vocabulary.txt"

        with patch(
            "transcribe.domain.vocabulary_loader.DEFAULT_VOCABULARY_PATH", vocab_path
        ):
            # When: initializing vocabulary file
            created, message = initialize_vocabulary_file()

        # Then: parent directories are created
        assert created is True
        assert vocab_path.parent.exists()
        assert vocab_path.exists()

    def test_skips_when_file_already_exists(self, tmp_path: Path) -> None:
        """Should skip creation and notify when file already exists."""
        # Given: an existing vocabulary file
        vocab_path = tmp_path / "vocabulary.txt"
        vocab_path.write_text("existing content")

        with patch(
            "transcribe.domain.vocabulary_loader.DEFAULT_VOCABULARY_PATH", vocab_path
        ):
            # When: initializing vocabulary file
            created, message = initialize_vocabulary_file()

        # Then: file is not overwritten
        assert created is False
        assert "already exists" in message
        assert vocab_path.read_text() == "existing content"

    def test_sample_vocabulary_contains_expected_terms(self) -> None:
        """Should have sample vocabulary with expected terms."""
        # Then: sample vocabulary contains expected terms
        assert "Claude Code" in SAMPLE_VOCABULARY
        assert "OpenAI" in SAMPLE_VOCABULARY
        assert "Codex" in SAMPLE_VOCABULARY
        assert SAMPLE_VOCABULARY.startswith("#")  # Starts with comment
