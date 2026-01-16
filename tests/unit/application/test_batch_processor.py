"""Tests for batch processor module."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from transcribe.application.batch_processor import (
    BatchResult,
    find_mp3_files,
    get_output_path,
    process_directory,
    should_skip_file,
)
from transcribe.application.protocols import TranscriptionClientProtocol


@pytest.mark.unit
class TestFindMp3Files:
    """Tests for find_mp3_files function."""

    def test_finds_mp3_files_in_directory(self, tmp_path: Path) -> None:
        """Should find MP3 files in a directory."""
        # Given: a directory with MP3 files
        (tmp_path / "audio1.mp3").touch()
        (tmp_path / "audio2.mp3").touch()
        (tmp_path / "other.txt").touch()

        # When: finding MP3 files
        result = find_mp3_files(tmp_path)

        # Then: only MP3 files are returned
        assert len(result) == 2
        assert all(f.suffix == ".mp3" for f in result)

    def test_finds_mp3_files_recursively(self, tmp_path: Path) -> None:
        """Should find MP3 files in subdirectories."""
        # Given: a directory with nested MP3 files
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "audio1.mp3").touch()
        (subdir / "audio2.mp3").touch()

        # When: finding MP3 files
        result = find_mp3_files(tmp_path)

        # Then: MP3 files from all levels are returned
        assert len(result) == 2

    def test_returns_sorted_list(self, tmp_path: Path) -> None:
        """Should return MP3 files in sorted order."""
        # Given: MP3 files in unsorted order
        (tmp_path / "z_audio.mp3").touch()
        (tmp_path / "a_audio.mp3").touch()
        (tmp_path / "m_audio.mp3").touch()

        # When: finding MP3 files
        result = find_mp3_files(tmp_path)

        # Then: files are sorted
        assert result == sorted(result)
        assert result[0].name == "a_audio.mp3"
        assert result[-1].name == "z_audio.mp3"

    def test_returns_empty_list_for_no_mp3s(self, tmp_path: Path) -> None:
        """Should return empty list when no MP3 files exist."""
        # Given: a directory with no MP3 files
        (tmp_path / "audio.wav").touch()
        (tmp_path / "document.txt").touch()

        # When: finding MP3 files
        result = find_mp3_files(tmp_path)

        # Then: empty list is returned
        assert result == []

    def test_handles_case_insensitive_extension(self, tmp_path: Path) -> None:
        """Should find MP3 files with different case extensions."""
        # Given: MP3 files with different case extensions
        (tmp_path / "audio1.mp3").touch()
        (tmp_path / "audio2.MP3").touch()
        (tmp_path / "audio3.Mp3").touch()

        # When: finding MP3 files
        result = find_mp3_files(tmp_path)

        # Then: all MP3 files are found regardless of case
        assert len(result) == 3

    def test_raises_file_not_found_for_nonexistent_directory(self) -> None:
        """Should raise FileNotFoundError for non-existent directory."""
        # Given: a non-existent directory
        nonexistent = Path("/nonexistent/directory")

        # When/Then: finding MP3 files raises FileNotFoundError
        with pytest.raises(FileNotFoundError) as exc_info:
            find_mp3_files(nonexistent)

        assert "Directory not found" in str(exc_info.value)

    def test_raises_not_a_directory_for_file(self, tmp_path: Path) -> None:
        """Should raise NotADirectoryError when path is a file."""
        # Given: a file path instead of directory
        file_path = tmp_path / "file.txt"
        file_path.touch()

        # When/Then: finding MP3 files raises NotADirectoryError
        with pytest.raises(NotADirectoryError) as exc_info:
            find_mp3_files(file_path)

        assert "Not a directory" in str(exc_info.value)


@pytest.mark.unit
class TestGetOutputPath:
    """Tests for get_output_path function."""

    def test_returns_srt_extension_for_srt_format(self, tmp_path: Path) -> None:
        """Should return path with .srt extension for SRT format."""
        # Given: an MP3 path
        mp3_path = tmp_path / "audio.mp3"

        # When: getting output path for SRT format
        result = get_output_path(mp3_path, "srt")

        # Then: path has .srt extension
        assert result == tmp_path / "audio.srt"

    def test_returns_txt_extension_for_text_format(self, tmp_path: Path) -> None:
        """Should return path with .txt extension for text format."""
        # Given: an MP3 path
        mp3_path = tmp_path / "audio.mp3"

        # When: getting output path for text format
        result = get_output_path(mp3_path, "text")

        # Then: path has .txt extension
        assert result == tmp_path / "audio.txt"

    def test_preserves_directory_structure(self, tmp_path: Path) -> None:
        """Should preserve the directory structure in output path."""
        # Given: an MP3 path in a subdirectory
        mp3_path = tmp_path / "subdir" / "nested" / "audio.mp3"

        # When: getting output path
        result = get_output_path(mp3_path, "srt")

        # Then: directory structure is preserved
        assert result == tmp_path / "subdir" / "nested" / "audio.srt"


@pytest.mark.unit
class TestShouldSkipFile:
    """Tests for should_skip_file function."""

    def test_returns_true_when_srt_exists(self, tmp_path: Path) -> None:
        """Should return True when SRT output already exists."""
        # Given: an MP3 file with existing SRT
        mp3_path = tmp_path / "audio.mp3"
        srt_path = tmp_path / "audio.srt"
        mp3_path.touch()
        srt_path.touch()

        # When: checking skip condition for SRT format
        result = should_skip_file(mp3_path, "srt")

        # Then: should skip
        assert result is True

    def test_returns_false_when_srt_not_exists(self, tmp_path: Path) -> None:
        """Should return False when SRT output doesn't exist."""
        # Given: an MP3 file without existing SRT
        mp3_path = tmp_path / "audio.mp3"
        mp3_path.touch()

        # When: checking skip condition for SRT format
        result = should_skip_file(mp3_path, "srt")

        # Then: should not skip
        assert result is False

    def test_returns_true_when_txt_exists(self, tmp_path: Path) -> None:
        """Should return True when text output already exists."""
        # Given: an MP3 file with existing TXT
        mp3_path = tmp_path / "audio.mp3"
        txt_path = tmp_path / "audio.txt"
        mp3_path.touch()
        txt_path.touch()

        # When: checking skip condition for text format
        result = should_skip_file(mp3_path, "text")

        # Then: should skip
        assert result is True

    def test_checks_correct_extension_per_format(self, tmp_path: Path) -> None:
        """Should check correct extension based on format."""
        # Given: an MP3 file with only SRT (no TXT)
        mp3_path = tmp_path / "audio.mp3"
        srt_path = tmp_path / "audio.srt"
        mp3_path.touch()
        srt_path.touch()

        # When: checking skip condition for text format
        result = should_skip_file(mp3_path, "text")

        # Then: should not skip (TXT doesn't exist)
        assert result is False


@pytest.mark.unit
class TestProcessDirectory:
    """Tests for process_directory function."""

    def test_processes_all_mp3_files(self, tmp_path: Path) -> None:
        """Should process all MP3 files in directory."""
        # Given: a directory with MP3 files and a mock client
        (tmp_path / "audio1.mp3").touch()
        (tmp_path / "audio2.mp3").touch()

        client: TranscriptionClientProtocol = MagicMock()

        # When: processing directory
        result = process_directory(tmp_path, client, "srt")

        # Then: all files are processed
        assert result.processed == 2
        assert result.skipped == 0
        assert result.failed == 0
        assert client.transcribe.call_count == 2

    def test_skips_files_with_existing_output(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Should skip files when output already exists."""
        # Given: MP3 files with some existing SRT files
        (tmp_path / "audio1.mp3").touch()
        (tmp_path / "audio1.srt").touch()  # Existing output
        (tmp_path / "audio2.mp3").touch()

        client: TranscriptionClientProtocol = MagicMock()

        # When: processing directory
        result = process_directory(tmp_path, client, "srt")

        # Then: one file is skipped, one is processed
        assert result.processed == 1
        assert result.skipped == 1
        assert client.transcribe.call_count == 1

        # And: skip message is printed
        captured = capsys.readouterr()
        assert "スキップ" in captured.out
        assert "audio1.mp3" in captured.out

    def test_returns_zero_counts_for_empty_directory(self, tmp_path: Path) -> None:
        """Should return zero counts for directory with no MP3 files."""
        # Given: an empty directory
        client: TranscriptionClientProtocol = MagicMock()

        # When: processing directory
        result = process_directory(tmp_path, client, "srt")

        # Then: all counts are zero
        assert result == BatchResult(processed=0, skipped=0, failed=0, errors=[])
        assert client.transcribe.call_count == 0

    def test_continues_processing_after_failure(self, tmp_path: Path) -> None:
        """Should continue processing after one file fails."""
        # Given: MP3 files with a client that fails on the first file
        (tmp_path / "audio1.mp3").touch()
        (tmp_path / "audio2.mp3").touch()

        client: TranscriptionClientProtocol = MagicMock()
        client.transcribe.side_effect = [
            RuntimeError("API error"),  # First file fails
            1,  # Second file succeeds
        ]

        # When: processing directory
        result = process_directory(tmp_path, client, "srt")

        # Then: one processed, one failed
        assert result.processed == 1
        assert result.failed == 1
        assert len(result.errors) == 1
        assert client.transcribe.call_count == 2

    def test_handles_nested_directories(self, tmp_path: Path) -> None:
        """Should process MP3 files in nested directories."""
        # Given: MP3 files in nested directories
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "audio1.mp3").touch()
        (subdir / "audio2.mp3").touch()

        client: TranscriptionClientProtocol = MagicMock()

        # When: processing directory
        result = process_directory(tmp_path, client, "srt")

        # Then: all files are processed
        assert result.processed == 2

    def test_raises_for_nonexistent_directory(self) -> None:
        """Should raise FileNotFoundError for non-existent directory."""
        # Given: a non-existent directory
        client: TranscriptionClientProtocol = MagicMock()

        # When/Then: processing raises FileNotFoundError
        with pytest.raises(FileNotFoundError):
            process_directory(Path("/nonexistent"), client, "srt")

    def test_raises_for_file_instead_of_directory(self, tmp_path: Path) -> None:
        """Should raise NotADirectoryError when path is a file."""
        # Given: a file path
        file_path = tmp_path / "file.txt"
        file_path.touch()
        client: TranscriptionClientProtocol = MagicMock()

        # When/Then: processing raises NotADirectoryError
        with pytest.raises(NotADirectoryError):
            process_directory(file_path, client, "srt")

    def test_prints_progress_messages(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Should print progress messages during processing."""
        # Given: an MP3 file
        (tmp_path / "audio.mp3").touch()
        client: TranscriptionClientProtocol = MagicMock()

        # When: processing directory
        process_directory(tmp_path, client, "srt")

        # Then: progress message is printed
        captured = capsys.readouterr()
        assert "処理中" in captured.out
        assert "audio.mp3" in captured.out

    def test_uses_correct_response_format(self, tmp_path: Path) -> None:
        """Should pass correct response format to client."""
        # Given: an MP3 file
        mp3_path = tmp_path / "audio.mp3"
        mp3_path.touch()

        client: TranscriptionClientProtocol = MagicMock()

        # When: processing with text format
        process_directory(tmp_path, client, "text")

        # Then: client is called with text format
        call_args = client.transcribe.call_args
        assert call_args[0][2] == "text"  # Third positional argument
