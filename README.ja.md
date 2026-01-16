# whisper-srt

MP3音声ファイルをOpenAI Whisper APIを使用してSRT字幕形式に変換するCLIツール。

[English](https://github.com/tomada1114/whisper-srt/blob/main/README.md) | 日本語

## 特徴

- シンプルなCLIでMP3からSRT/テキストに変換
- OpenAI Whisper API (`whisper-1`) による高精度な文字起こし
- AI/技術用語の組み込み語彙で認識精度向上
- カスタム語彙対応
- バッチ処理: ディレクトリ内のMP3を再帰的に一括処理

## クイックスタート

**インストール不要** - [uv](https://docs.astral.sh/uv/)で即実行:

```bash
# OpenAI APIキーを設定
export OPENAI_API_KEY="your-api-key"

# 文字起こし（audio.srtが作成される）
uvx whisper-srt audio.mp3
```

APIキーは [OpenAI Platform](https://platform.openai.com/api-keys) で取得できます。

## インストール（任意）

永続的にインストールしたい場合:

```bash
uv tool install whisper-srt
whisper-srt audio.mp3
```

> **注意**: `Executable already exists`エラーが出た場合は、`--force`で上書きしてください:
> ```bash
> uv tool install whisper-srt --force
> ```

## アップグレード

インストール済みの場合、最新版にアップグレード:

```bash
uv tool upgrade whisper-srt
```

## 使い方

```bash
whisper-srt input.mp3                    # 基本的な使い方（デフォルト: 英語）
whisper-srt input.mp3 -o output.srt      # 出力ファイルを指定
whisper-srt input.mp3 --language ja      # 言語を指定（日本語）
whisper-srt input.mp3 --text             # プレーンテキストで出力（input.txt）
whisper-srt --dir ./recordings           # ディレクトリ内のMP3を一括処理
whisper-srt --help                       # 全オプションを確認
```

### バッチ処理

`--dir`オプションでディレクトリ内のMP3ファイルを再帰的に処理:

```bash
whisper-srt --dir ./recordings              # 全MP3をSRTに変換
whisper-srt --dir ./recordings --text       # 全MP3をテキストに変換
whisper-srt --dir ./recordings --language ja  # 日本語で処理
```

- サブディレクトリも再帰的に探索
- 出力ファイルは元のMP3と同じ場所に保存
- 既存の出力ファイルは自動でスキップ
- 進捗表示: `処理中: file.mp3` / `スキップ: file.mp3（既存）`

## 初期設定

`--init`で対話的にデフォルト設定を行います:

```bash
whisper-srt --init
```

このコマンドは以下を実行します:
1. `~/.config/whisper-srt/vocabulary.txt`に語彙ファイルを作成
2. デフォルト言語を選択（`~/.config/whisper-srt/language.txt`に保存）

設定後は、毎回`--language`オプションを指定する必要がなくなります。

## 対応言語

デフォルト言語は**英語 (`en`)** です。

主要な言語コード（ISO-639-1）:
| コード | 言語 | コード | 言語 |
|--------|------|--------|------|
| `en` | 英語 | `ja` | 日本語 |
| `zh` | 中国語 | `ko` | 韓国語 |
| `es` | スペイン語 | `fr` | フランス語 |
| `de` | ドイツ語 | `pt` | ポルトガル語 |

全対応言語は [OpenAI Whisperドキュメント](https://platform.openai.com/docs/guides/speech-to-text) を参照してください。

## カスタム語彙

`~/.config/whisper-srt/vocabulary.txt` に専門用語を登録:

```
YouTube
ポッドキャスト
自社製品名
```

## 料金

$0.006/分（1時間あたり約$0.36）

## 開発

```bash
git clone https://github.com/tomada1114/whisper-srt.git
cd whisper-srt
uv sync --dev
make ci   # lint + type-check + test
```

## ライセンス

MIT
