"""Command-line interface for transcription.

This module provides the CLI entry point for transcribing
MP3 audio files to SRT subtitle format.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from transcribe.domain.vocabulary import DEFAULT_VOCABULARY
from transcribe.infrastructure.whisper_client import WhisperTranscriptionClient

logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="transcribe",
        description="Transcribe MP3 audio to SRT subtitle format using Whisper.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  transcribe input.mp3                        # Output: input_transcribed.srt
  transcribe input.mp3 -o output.srt          # Specify output file
  transcribe input.mp3 --model medium         # Use medium model (faster)
  transcribe input.mp3 --language en          # English transcription
  transcribe input.mp3 --vocabulary vocab.txt # Custom vocabulary file
        """,
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input MP3 file path",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output SRT file path (default: {input_stem}_transcribed.srt)",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="large",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: large)",
    )

    parser.add_argument(
        "--language",
        type=str,
        default="Japanese",
        help="Target language for transcription (default: Japanese)",
    )

    parser.add_argument(
        "--vocabulary",
        type=Path,
        default=None,
        help="Custom vocabulary file (one term per line)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    return parser


def load_vocabulary(path: Path | None) -> tuple[str, ...]:
    """Load vocabulary from file or return default.

    Args:
        path: Path to vocabulary file, or None for default.

    Returns:
        Tuple of vocabulary terms.

    Raises:
        FileNotFoundError: If vocabulary file does not exist.
    """
    if path is None:
        return DEFAULT_VOCABULARY

    if not path.exists():
        msg = f"Vocabulary file not found: {path}"
        raise FileNotFoundError(msg)

    content = path.read_text(encoding="utf-8")
    terms = [line.strip() for line in content.splitlines() if line.strip()]
    return tuple(terms)


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: Command-line arguments (default: sys.argv[1:]).

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )

    # Validate input file
    input_path: Path = args.input
    if not input_path.exists():
        logger.error("Input file not found: %s", input_path)
        return 1

    if not input_path.suffix.lower() == ".mp3":
        logger.warning("Input file does not have .mp3 extension: %s", input_path)

    # Determine output path
    output_path: Path | None = args.output
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_transcribed.srt"

    # Load vocabulary
    try:
        vocabulary = load_vocabulary(args.vocabulary)
        logger.debug("Loaded %d vocabulary terms", len(vocabulary))
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    # Create client and transcribe
    client = WhisperTranscriptionClient(
        model_size=args.model,
        language=args.language,
        vocabulary=vocabulary,
    )

    try:
        logger.info("Transcribing %s...", input_path)
        segment_count = client.transcribe(input_path, output_path)
        logger.info("Generated %d segments: %s", segment_count, output_path)
        print(f"Transcription complete: {segment_count} segments saved to {output_path}")
        return 0

    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
        return 1

    except RuntimeError as e:
        logger.error("Transcription failed: %s", e)
        return 1

    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        return 130


if __name__ == "__main__":
    sys.exit(main())
