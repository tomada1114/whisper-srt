# Ticket #9: Create Japanese README (README.ja.md)

## Overview
Create a Japanese version of the README for Japanese-speaking users.

## Acceptance Criteria
- [ ] README.ja.md created with Japanese content
- [ ] Link from main README.md to Japanese version
- [ ] Same structure as English README
- [ ] Japanese-specific notes if applicable

## README.ja.md Structure

```markdown
# whisper-srt

MP3音声ファイルをOpenAI Whisper APIを使用してSRT字幕形式に変換するCLIツール。

[English](README.md) | 日本語

## 特徴

- シンプルなCLIでMP3からSRTに変換
- 自動言語検出または手動指定
- カスタム語彙で認識精度を向上
- 非対話式（バッチ処理に対応）

## インストール

### pipx（推奨）
\`\`\`bash
pipx install whisper-srt
\`\`\`

### pip
\`\`\`bash
pip install whisper-srt
\`\`\`

## クイックスタート

1. OpenAI APIキーを設定:
\`\`\`bash
export OPENAI_API_KEY="your-api-key"
\`\`\`

2. 音声ファイルを文字起こし:
\`\`\`bash
whisper-srt audio.mp3
\`\`\`

同じディレクトリに `audio.srt` が作成されます。

## 使い方

\`\`\`bash
# 基本的な使い方（input.srtを出力）
whisper-srt input.mp3

# 出力ファイルを指定
whisper-srt input.mp3 -o output.srt

# 言語を指定
whisper-srt input.mp3 --language ja

# カスタム語彙ファイルを使用
whisper-srt input.mp3 --vocabulary ~/my-vocab.txt

# 語彙を無効化
whisper-srt input.mp3 --no-vocabulary

# 詳細出力
whisper-srt input.mp3 -v
\`\`\`

## 設定

### APIキー
環境変数 `OPENAI_API_KEY` を設定するか、`.env` ファイルを作成:
\`\`\`
OPENAI_API_KEY=sk-...
\`\`\`

### カスタム語彙
`~/.config/whisper-srt/vocabulary.txt` を作成し、1行に1語ずつ記載:
\`\`\`
YouTube
ポッドキャスト
チュートリアル
# コメントは#で始める
\`\`\`

## 対応言語

| コード | 言語 |
|--------|------|
| en | 英語（デフォルト） |
| ja | 日本語 |
| zh | 中国語 |
| es | スペイン語 |
| fr | フランス語 |
| de | ドイツ語 |
| ko | 韓国語 |

全リストは[Whisperドキュメント](https://platform.openai.com/docs/guides/speech-to-text)を参照。

## ライセンス

MIT

## 開発への参加

開発環境のセットアップとガイドラインは [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。
```

## Files to Create/Modify
- `README.ja.md` - New file
- `README.md` - Add link to Japanese version

## Link in README.md
Add at the top:
```markdown
English | [日本語](README.ja.md)
```

## Dependencies
- Ticket #8 (English README) should be completed first
