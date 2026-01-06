"""Tests for configuration file loader."""

from pathlib import Path
from unittest.mock import patch

import pytest

from transcribe.domain.config_loader import (
    DEFAULT_LANGUAGE,
    DEFAULT_LANGUAGE_PATH,
    SUPPORTED_LANGUAGES,
    load_default_language,
    prompt_language_selection,
    save_language,
)


@pytest.mark.unit
class TestLoadDefaultLanguage:
    """Tests for load_default_language function."""

    def test_returns_default_when_file_not_exists(self) -> None:
        """Should return DEFAULT_LANGUAGE when config file doesn't exist."""
        # Given: config file that doesn't exist
        with patch.object(Path, "exists", return_value=False):
            # When: loading default language
            result = load_default_language()

        # Then: default language (en) is returned
        assert result == DEFAULT_LANGUAGE

    def test_loads_language_from_file(self, tmp_path: Path) -> None:
        """Should load language from config file when it exists."""
        # Given: a config file with Japanese language
        config_file = tmp_path / "language.txt"
        config_file.write_text("ja\n")

        with patch(
            "transcribe.domain.config_loader.DEFAULT_LANGUAGE_PATH", config_file
        ):
            # When: loading default language
            result = load_default_language()

        # Then: Japanese is returned
        assert result == "ja"

    def test_strips_whitespace_from_language(self, tmp_path: Path) -> None:
        """Should strip whitespace from language code."""
        # Given: a config file with whitespace
        config_file = tmp_path / "language.txt"
        config_file.write_text("  ko  \n")

        with patch(
            "transcribe.domain.config_loader.DEFAULT_LANGUAGE_PATH", config_file
        ):
            # When: loading default language
            result = load_default_language()

        # Then: Korean without whitespace is returned
        assert result == "ko"

    def test_returns_default_when_file_is_empty(self, tmp_path: Path) -> None:
        """Should return default when config file is empty."""
        # Given: an empty config file
        config_file = tmp_path / "language.txt"
        config_file.write_text("")

        with patch(
            "transcribe.domain.config_loader.DEFAULT_LANGUAGE_PATH", config_file
        ):
            # When: loading default language
            result = load_default_language()

        # Then: default language is returned
        assert result == DEFAULT_LANGUAGE

    def test_default_language_path_is_correct(self) -> None:
        """Should have correct default language path."""
        # Then: default path is ~/.config/whisper-srt/language.txt
        expected = Path.home() / ".config" / "whisper-srt" / "language.txt"
        assert DEFAULT_LANGUAGE_PATH == expected


@pytest.mark.unit
class TestSaveLanguage:
    """Tests for save_language function."""

    def test_saves_language_to_file(self, tmp_path: Path) -> None:
        """Should save language code to config file."""
        # Given: a config directory path
        config_dir = tmp_path / ".config" / "whisper-srt"
        config_file = config_dir / "language.txt"

        with patch(
            "transcribe.domain.config_loader.DEFAULT_CONFIG_DIR", config_dir
        ), patch("transcribe.domain.config_loader.DEFAULT_LANGUAGE_PATH", config_file):
            # When: saving language
            save_language("ja")

        # Then: language is saved to file
        assert config_file.exists()
        assert config_file.read_text() == "ja\n"

    def test_creates_parent_directory(self, tmp_path: Path) -> None:
        """Should create parent directory if it doesn't exist."""
        # Given: a non-existent config directory
        config_dir = tmp_path / "deep" / "nested" / "config"
        config_file = config_dir / "language.txt"

        with patch(
            "transcribe.domain.config_loader.DEFAULT_CONFIG_DIR", config_dir
        ), patch("transcribe.domain.config_loader.DEFAULT_LANGUAGE_PATH", config_file):
            # When: saving language
            save_language("fr")

        # Then: parent directories are created
        assert config_dir.exists()
        assert config_file.exists()

    def test_overwrites_existing_file(self, tmp_path: Path) -> None:
        """Should overwrite existing config file."""
        # Given: an existing config file
        config_dir = tmp_path
        config_file = config_dir / "language.txt"
        config_file.write_text("en\n")

        with patch(
            "transcribe.domain.config_loader.DEFAULT_CONFIG_DIR", config_dir
        ), patch("transcribe.domain.config_loader.DEFAULT_LANGUAGE_PATH", config_file):
            # When: saving new language
            save_language("de")

        # Then: file is overwritten
        assert config_file.read_text() == "de\n"


@pytest.mark.unit
class TestPromptLanguageSelection:
    """Tests for prompt_language_selection function."""

    def test_selects_language_by_number(self) -> None:
        """Should select language by number input."""
        # Given: user inputs number 2 (Japanese)
        with patch("builtins.input", return_value="2"):
            # When: prompting for selection
            result = prompt_language_selection()

        # Then: Japanese is returned
        assert result == "ja"

    def test_selects_language_by_code(self) -> None:
        """Should select language by code input."""
        # Given: user inputs language code
        with patch("builtins.input", return_value="ko"):
            # When: prompting for selection
            result = prompt_language_selection()

        # Then: Korean is returned
        assert result == "ko"

    def test_returns_english_on_empty_input(self) -> None:
        """Should return English when user presses Enter."""
        # Given: user presses Enter (empty input)
        with patch("builtins.input", return_value=""):
            # When: prompting for selection
            result = prompt_language_selection()

        # Then: English is returned
        assert result == "en"

    def test_returns_english_on_eof(self) -> None:
        """Should return English on EOF (Ctrl+D)."""
        # Given: user presses Ctrl+D (EOF)
        with patch("builtins.input", side_effect=EOFError):
            # When: prompting for selection
            result = prompt_language_selection()

        # Then: English is returned
        assert result == "en"

    def test_accepts_custom_language_code(self) -> None:
        """Should accept custom language code not in list."""
        # Given: user inputs custom language code
        with patch("builtins.input", return_value="th"):
            # When: prompting for selection
            result = prompt_language_selection()

        # Then: custom code is returned
        assert result == "th"

    def test_retries_on_invalid_number(self) -> None:
        """Should retry when invalid number is entered."""
        # Given: user enters invalid number then valid number
        with patch("builtins.input", side_effect=["99", "3"]):
            # When: prompting for selection
            result = prompt_language_selection()

        # Then: Chinese is returned (3rd option)
        assert result == "zh"

    def test_supported_languages_contains_expected_entries(self) -> None:
        """Should have expected languages in supported list."""
        # Then: supported languages contain expected entries
        codes = [code for code, _ in SUPPORTED_LANGUAGES]
        assert "en" in codes
        assert "ja" in codes
        assert "zh" in codes
        assert "ko" in codes
