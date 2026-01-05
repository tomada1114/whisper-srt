# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MP3音声ファイルをWhisperでSRT字幕形式に変換するCLIツール。stable-tsを使用して正確なタイミングの字幕を生成する。

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
pytest tests/unit/infrastructure/test_whisper_client.py::test_transcribe_success -v

# 文字起こし実行
python -m transcribe input.mp3
python -m transcribe input.mp3 -o output.srt --model medium
```

## Architecture

Onion Architecture with Protocol-based dependency injection:

```
src/transcribe/
├── domain/           # ドメイン層: vocabulary.py（組み込み語彙定義）
├── application/      # アプリケーション層: protocols.py（TranscriptionClientProtocol）
├── infrastructure/   # インフラ層: whisper_client.py（stable-ts実装）, mock_client.py
└── interface/        # インターフェース層: cli.py（CLIエントリーポイント）
```

**Key patterns:**
- `TranscriptionClientProtocol`: 文字起こしクライアントの契約を定義。WhisperTranscriptionClientが実装
- 語彙プロンプト: DEFAULT_VOCABULARY（AI/MCP技術用語）をWhisperのinitial_promptに渡して認識精度を向上
- stable-tsの`split_by_length(max_chars=24)`で読みやすい字幕分割

## Testing

- `tests/unit/`: ユニットテスト
- `pytest-mock`でWhisperモデルをモック化（実際のモデルロード不要）
- markers: `@pytest.mark.unit`, `@pytest.mark.slow`
