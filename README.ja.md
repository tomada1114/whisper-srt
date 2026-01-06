# whisper-srt

MP3音声ファイルをOpenAI Whisper APIを使用してSRT字幕形式に変換するCLIツール。

[English](README.md) | 日本語

## 特徴

- シンプルなCLIでMP3からSRTに変換
- OpenAI Whisper API (`whisper-1`) による高精度な文字起こし
- 自動言語検出または手動指定
- カスタム語彙で認識精度を向上
- AI/技術用語の組み込み語彙
- 非対話式（バッチ処理に対応）

## 料金

- $0.006/分（1時間あたり約$0.36）
- 新規OpenAIアカウントには無料クレジット付与あり

## インストール

### pipx（推奨）

依存関係の競合を避けた隔離環境でインストール:

```bash
pipx install whisper-srt
```

### pip

```bash
pip install whisper-srt
```

### ソースから（開発用）

```bash
git clone https://github.com/tomada1114/whisper-srt.git
cd whisper-srt
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## クイックスタート

1. OpenAI APIキーを設定:
```bash
export OPENAI_API_KEY="your-api-key"
```

2. 音声ファイルを文字起こし:
```bash
whisper-srt audio.mp3
```

同じディレクトリに `audio.srt` が作成されます。

## 使い方

```bash
# 基本的な使い方（input.srtを出力）
whisper-srt input.mp3

# 出力ファイルを指定
whisper-srt input.mp3 -o output.srt

# 言語を指定（ISO-639-1コード）
whisper-srt input.mp3 --language ja

# カスタム語彙ファイルを使用
whisper-srt input.mp3 --vocabulary ~/my-vocab.txt

# 語彙を無効化
whisper-srt input.mp3 --no-vocabulary

# 詳細出力
whisper-srt input.mp3 -v
```

### オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `-o, --output` | 出力SRTファイルパス | `{入力ファイル名}.srt` |
| `--language` | 言語コード（ISO-639-1） | `ja` |
| `--vocabulary` | カスタム語彙ファイルパス | なし |
| `--no-vocabulary` | 語彙プロンプトを無効化 | オフ |
| `-v, --verbose` | 詳細ログ出力 | オフ |

## 設定

### APIキー

以下のいずれかの方法でOpenAI APIキーを設定:

#### 方法1: 環境変数（pipx利用時に推奨）

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

シェル設定ファイル（`~/.zshrc` や `~/.bashrc`）に追加すると永続化できます。

#### 方法2: .envファイル（プロジェクト単位）

```bash
cp .env.example .env
# .env を編集して OPENAI_API_KEY を設定
```

APIキーは [OpenAI Platform](https://platform.openai.com/api-keys) で取得できます。

### カスタム語彙

`~/.config/whisper-srt/vocabulary.txt` を作成し、1行に1語ずつ記載:

```
YouTube
ポッドキャスト
チュートリアル
# コメントは#で始める
```

### 組み込み語彙

以下のカテゴリのAI/技術用語が組み込まれており、認識精度を向上させます：

- AIサービス（Claude, ChatGPT, Gemini等）
- AIコーディングツール（Cursor, Windsurf, Cline等）
- MCP関連（Model Context Protocol, MCP Connector等）
- Claude Code機能（CLAUDE.md, サブエージェント, hooks等）
- 開発手法（DDD, Onion Architecture, AI駆動開発等）

## 対応言語

| コード | 言語 |
|--------|------|
| en | 英語 |
| ja | 日本語（デフォルト） |
| zh | 中国語 |
| es | スペイン語 |
| fr | フランス語 |
| de | ドイツ語 |
| ko | 韓国語 |

全リストは[Whisperドキュメント](https://platform.openai.com/docs/guides/speech-to-text)を参照。

## 開発

```bash
make help        # ヘルプを表示
make ci          # lint + type-check + test を実行
make test        # テストを実行
make test-cov    # カバレッジ付きでテストを実行
make lint        # linterを実行
make format      # コードをフォーマット
make type-check  # 型チェックを実行
```

## 依存関係

- Python 3.9+
- openai
- python-dotenv

## ライセンス

MIT

## 開発への参加

開発環境のセットアップとガイドラインは [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。
