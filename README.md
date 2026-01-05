# transcribe-srt

MP3音声ファイルをWhisperでSRT字幕形式に変換するCLIツール。

## インストール

```bash
# 開発用インストール
pip install -e ".[dev]"

# 本番用インストール
pip install -e .
```

## 使い方

```bash
# 基本的な使い方
python -m transcribe input.mp3

# 出力ファイルを指定
python -m transcribe input.mp3 -o output.srt

# モデルサイズを変更（tiny, base, small, medium, large）
python -m transcribe input.mp3 --model medium

# 言語を指定
python -m transcribe input.mp3 --language en

# カスタム語彙ファイルを使用
python -m transcribe input.mp3 --vocabulary custom_vocab.txt

# 詳細ログを有効化
python -m transcribe input.mp3 -v
```

## Makeコマンド

```bash
make help        # ヘルプを表示
make dev         # 開発用依存関係をインストール
make ci          # lint + type-check + test を実行
make test        # テストを実行
make test-cov    # カバレッジ付きでテストを実行
make lint        # linterを実行
make format      # コードをフォーマット
make type-check  # 型チェックを実行
```

## 語彙ファイル形式

カスタム語彙ファイルは1行に1単語のテキストファイルです：

```
Claude
Claude Code
MCP
Model Context Protocol
```

## 機能

- Whisper large モデルによる高精度な文字起こし
- stable-ts による正確なタイミング調整
- 日本語技術用語（AI/MCP関連）の組み込み語彙
- カスタム語彙ファイルのサポート
- モデルサイズ・言語の設定可能

## 依存関係

- Python 3.9+
- openai-whisper
- stable-ts
