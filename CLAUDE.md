# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MP3音声ファイルをOpenAI Whisper API（whisper-1）でSRT字幕形式に変換するCLIツール。

## Commands

```bash
# 開発環境セットアップ
source venv/bin/activate
pip install -e ".[dev]"

# CI実行（lint + type-check + test）
make ci

# 個別実行
make lint          # ruff check
make format        # ruff format + check --fix
make type-check    # mypy
make test          # pytest
make test-cov      # pytest with coverage

# 単一テスト実行
pytest tests/unit/domain/test_vocabulary.py -v
pytest tests/unit/infrastructure/test_openai_client.py::test_transcribe_creates_srt_file -v

# 文字起こし実行
python -m transcribe input.mp3
python -m transcribe input.mp3 -o output.srt --language en
```

## Architecture

Onion Architecture with Protocol-based dependency injection:

```
src/transcribe/
├── domain/           # ドメイン層: vocabulary.py（組み込み語彙定義）
├── application/      # アプリケーション層: protocols.py（TranscriptionClientProtocol）
├── infrastructure/   # インフラ層: openai_client.py（OpenAI Whisper API実装）
└── interface/        # インターフェース層: cli.py（CLIエントリーポイント）
```

**Key patterns:**
- `TranscriptionClientProtocol`: 文字起こしクライアントの契約を定義。OpenAITranscriptionClientが実装
- 語彙プロンプト: DEFAULT_VOCABULARY（AI/MCP技術用語）をWhisper APIのpromptパラメータに渡して認識精度を向上

## Testing

- `tests/unit/`: ユニットテスト
- `pytest-mock`でOpenAI APIをモック化（実際のAPI呼び出し不要）
- markers: `@pytest.mark.unit`, `@pytest.mark.slow`
