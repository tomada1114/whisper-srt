"""Batch processing for directory transcription.

This module provides batch processing capabilities for transcribing
multiple MP3 files in a directory structure.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from transcribe.application.protocols import ResponseFormat, TranscriptionClientProtocol

__all__ = ["BatchResult", "find_mp3_files", "process_directory"]

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BatchResult:
    """Result of batch processing operation."""

    processed: int
    skipped: int
    failed: int
    errors: list[tuple[Path, str]]


def find_mp3_files(directory: Path) -> list[Path]:
    """Find all MP3 files recursively in a directory.

    Args:
        directory: Root directory to search.

    Returns:
        List of MP3 file paths, sorted for deterministic ordering.

    Raises:
        FileNotFoundError: If directory does not exist.
        NotADirectoryError: If path is not a directory.
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    # Case-insensitive matching for cross-platform consistency
    all_files = list(directory.rglob("*"))
    mp3_files = [f for f in all_files if f.is_file() and f.suffix.lower() == ".mp3"]
    return sorted(mp3_files)


def get_output_path(mp3_path: Path, response_format: ResponseFormat) -> Path:
    """Determine output path for an MP3 file.

    Args:
        mp3_path: Path to input MP3 file.
        response_format: Output format ("srt" or "text").

    Returns:
        Output path with appropriate extension.
    """
    extension = ".txt" if response_format == "text" else ".srt"
    return mp3_path.with_suffix(extension)


def should_skip_file(mp3_path: Path, response_format: ResponseFormat) -> bool:
    """Check if output file already exists (skip condition).

    Args:
        mp3_path: Path to input MP3 file.
        response_format: Output format to check.

    Returns:
        True if output file exists and should be skipped.
    """
    output_path = get_output_path(mp3_path, response_format)
    return output_path.exists()


def process_directory(
    directory: Path,
    client: TranscriptionClientProtocol,
    response_format: ResponseFormat = "srt",
) -> BatchResult:
    """Process all MP3 files in a directory.

    Args:
        directory: Root directory containing MP3 files.
        client: Transcription client to use.
        response_format: Output format for all files.

    Returns:
        BatchResult with counts and error details.

    Raises:
        FileNotFoundError: If directory does not exist.
        NotADirectoryError: If path is not a directory.
    """
    mp3_files = find_mp3_files(directory)

    if not mp3_files:
        logger.warning("No MP3 files found in: %s", directory)
        return BatchResult(processed=0, skipped=0, failed=0, errors=[])

    processed = 0
    skipped = 0
    failed = 0
    errors: list[tuple[Path, str]] = []

    for mp3_path in mp3_files:
        output_path = get_output_path(mp3_path, response_format)

        # Check skip condition
        if output_path.exists():
            print(f"スキップ: {mp3_path.name}（{output_path.name} 既存）")
            skipped += 1
            continue

        # Process file
        print(f"処理中: {mp3_path.name}")

        try:
            client.transcribe(mp3_path, output_path, response_format)
            processed += 1
        except KeyboardInterrupt:
            raise
        except Exception as e:
            error_msg = str(e)
            logger.error("Failed to process %s: %s", mp3_path, error_msg)
            print(f"エラー: {mp3_path.name} - {error_msg}")
            errors.append((mp3_path, error_msg))
            failed += 1

    return BatchResult(
        processed=processed,
        skipped=skipped,
        failed=failed,
        errors=errors,
    )
