"""Command-line interface for transcription.

This module provides the CLI entry point for transcribing
MP3 audio files to SRT subtitle or plain text format using OpenAI Whisper API.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from transcribe import __version__
from transcribe.application.batch_processor import process_directory
from transcribe.application.protocols import ResponseFormat, TranscriptionClientProtocol
from transcribe.domain.audio_formats import SUPPORTED_AUDIO_EXTENSIONS
from transcribe.domain.config_loader import (
    load_default_language,
    prompt_language_selection,
    save_language,
)
from transcribe.domain.vocabulary_loader import (
    initialize_vocabulary_file,
    load_default_vocabulary,
    load_vocabulary_from_file,
)
from transcribe.infrastructure.openai_client import OpenAITranscriptionClient

logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="whisper-srt",
        description="Transcribe audio files to SRT subtitle format using OpenAI Whisper API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  whisper-srt input.mp3                       # Output: input.srt
  whisper-srt input.mp3 -o output.srt         # Specify output file
  whisper-srt input.mp3 --language en         # English transcription
  whisper-srt input.mp3 --text                # Output as plain text: input.txt
  whisper-srt --dir ./recordings              # Process all MP3s in directory
  whisper-srt --dir ./recordings --text       # Process all MP3s as text
        """,
    )

    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=None,
        help="Input audio file path (mp3, webm, wav, m4a, ogg, flac, mp4, mpeg, mpga, oga)",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file path (default: {input_stem}.srt, or .txt with --text)",
    )

    parser.add_argument(
        "--language",
        type=str,
        default=None,
        help="Target language code for transcription (ISO-639-1, default: from config or en)",
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
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize vocabulary file at ~/.config/whisper-srt/vocabulary.txt",
    )

    vocab_group = parser.add_mutually_exclusive_group()
    vocab_group.add_argument(
        "--vocabulary",
        type=Path,
        default=None,
        help="Path to vocabulary file (one word per line)",
    )
    vocab_group.add_argument(
        "--no-vocabulary",
        action="store_true",
        help="Disable vocabulary loading",
    )

    parser.add_argument(
        "--text",
        action="store_true",
        help="Output as plain text instead of SRT",
    )

    parser.add_argument(
        "--dir",
        type=Path,
        default=None,
        metavar="PATH",
        help="Directory to process audio files recursively (output in same location)",
    )

    return parser


def _load_vocabulary(args: argparse.Namespace) -> tuple[str, ...] | None:
    """Load vocabulary based on CLI arguments.

    Returns:
        Vocabulary tuple, or None if vocabulary file not found.
    """
    if args.no_vocabulary:
        return ()
    if args.vocabulary:
        try:
            return load_vocabulary_from_file(args.vocabulary)
        except FileNotFoundError:
            logger.error("Vocabulary file not found: %s", args.vocabulary)
            return None
    return load_default_vocabulary()


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

    # Handle --init option
    if args.init:
        created, message = initialize_vocabulary_file()
        print(message)

        language = prompt_language_selection()
        save_language(language)
        print(f"\nLanguage setting saved: {language}")
        return 0

    # Validate mutual exclusivity
    if args.dir is not None and args.input is not None:
        parser.error("--dir and input file are mutually exclusive")

    if args.dir is not None and args.output is not None:
        parser.error("--dir and --output are mutually exclusive")

    # Validate input argument
    if args.dir is None and args.input is None:
        parser.error("the following arguments are required: input or --dir")

    # Variables for single file mode
    input_path: Path | None = None
    output_path: Path | None = None

    # Validate input file (single file mode only)
    if args.input is not None:
        input_path = args.input
        if not input_path.exists():
            logger.error("Input file not found: %s", input_path)
            return 1

        if input_path.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:
            supported = ", ".join(sorted(SUPPORTED_AUDIO_EXTENSIONS))
            logger.error(
                "Unsupported audio format '%s'. Supported formats: %s",
                input_path.suffix,
                supported,
            )
            return 1

        # Determine output path
        output_path = args.output
        if output_path is None:
            extension = ".txt" if args.text else ".srt"
            output_path = input_path.with_suffix(extension)

    # Load vocabulary
    vocabulary = _load_vocabulary(args)
    if vocabulary is None:
        return 1

    if vocabulary:
        logger.debug("Loaded %d vocabulary terms", len(vocabulary))

    # Determine language
    language = args.language if args.language else load_default_language()
    logger.debug("Using language: %s", language)

    # Create client
    try:
        client: TranscriptionClientProtocol = OpenAITranscriptionClient(
            language=language, vocabulary=vocabulary
        )
    except ValueError as e:
        logger.error(str(e))
        return 1

    response_format: ResponseFormat = "text" if args.text else "srt"

    # Directory processing mode
    if args.dir is not None:
        return _process_directory(args.dir, client, response_format)

    # Single file processing mode
    assert input_path is not None  # Guaranteed by earlier validation
    assert output_path is not None  # Guaranteed by earlier validation
    return _process_single_file(input_path, output_path, client, response_format)


def _process_single_file(
    input_path: Path,
    output_path: Path,
    client: TranscriptionClientProtocol,
    response_format: ResponseFormat,
) -> int:
    """Process single file and return exit code."""
    try:
        logger.info("Transcribing %s...", input_path)
        segment_count = client.transcribe(input_path, output_path, response_format)
        if response_format == "text":
            logger.info("Transcription saved to %s", output_path)
            print(f"Transcription complete: saved to {output_path}")
        else:
            logger.info("Generated %d segments: %s", segment_count, output_path)
            print(f"Transcription complete: {segment_count} segments saved to {output_path}")
        return 0

    except (FileNotFoundError, RuntimeError) as e:
        logger.error("%s", e)
        return 1

    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        return 130


def _process_directory(
    directory: Path,
    client: TranscriptionClientProtocol,
    response_format: ResponseFormat,
) -> int:
    """Process directory and return exit code."""
    try:
        result = process_directory(directory, client, response_format)
    except (FileNotFoundError, NotADirectoryError) as e:
        logger.error(str(e))
        return 1
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        return 130

    # Summary
    print(f"\n完了: {result.processed}件処理, {result.skipped}件スキップ, {result.failed}件失敗")

    return 1 if result.failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
