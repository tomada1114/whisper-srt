"""Default vocabulary for transcription accuracy improvement.

This module contains domain-specific technical terms organized by category
that improve Whisper's recognition accuracy for AI-driven development content.

Categories are defined as separate tuples for easier maintenance and updates.
The build_vocabulary() function combines all categories into a single tuple.
"""

# =============================================================================
# AI サービス・プラットフォーム
# =============================================================================
AI_SERVICES: tuple[str, ...] = (
    # Claude 関連
    "Claude",
    "Claude Code",
    "Claude Sonnet",
    "Claude Sonnet 4",
    "Claude Sonnet 4.5",
    "Claude Opus",
    "Claude Opus 4",
    "Claude Opus 4.5",
    "Claude Haiku",
    "Claude Haiku 4.5",
    "Claude Pro",
    "Claude Max",
    "Anthropic",
    # OpenAI 関連
    "ChatGPT",
    "GPT-4",
    "GPT-4o",
    "GPT-5",
    "OpenAI",
    "Whisper",
    # その他 AI サービス
    "Gemini",
    "Gemini CLI",
    "Perplexity",
    "DeepSeek",
    # API・SDK 関連
    "Messages API",
    "Agent SDK",
    "Claude Agent SDK",
    "OpenAI Agents SDK",
    "Prompt Caching",
    "Structured Outputs",
    "Extended Thinking",
    # LLM 関連
    "LLM",
    "Large Language Model",
    "RAG",
    "Fine-tuning",
    "Chain-of-Thought",
    "生成AI",
)

# =============================================================================
# AI コーディングツール・エージェント
# =============================================================================
CODING_TOOLS: tuple[str, ...] = (
    "Cursor",
    "Windsurf",
    "Cline",
    "Codex",
    "Codex CLI",
    "GitHub Copilot",
    "Bolt.new",
    "Lovable.dev",
    "v0",
    "Replit",
    "Kiro",
)

# =============================================================================
# MCP (Model Context Protocol) 関連
# =============================================================================
MCP_TERMS: tuple[str, ...] = (
    "MCP",
    "Model Context Protocol",
    "MCP Connector",
    "Playwright MCP",
    "filesystem MCP",
    "Slack MCP",
    "Desktop Commander",
    "Serena",
    "Context7",
    "Supabase MCP",
    "Brave Search MCP",
    "Obsidian MCP",
    "GitHub MCP",
)

# =============================================================================
# Claude Code 機能・コンポーネント
# =============================================================================
CLAUDE_CODE_TERMS: tuple[str, ...] = (
    # ファイル・ディレクトリ
    "CLAUDE.md",
    ".claude",
    ".claude/",
    ".claude/rules",
    ".claude/rules/",
    ".claude/commands",
    ".claude/commands/",
    ".claude/agents",
    ".claude/agents/",
    ".mcp.json",
    ".claudeignore",
    "claude_desktop_config.json",
    # 機能・コンポーネント
    "サブエージェント",
    "Sub agents",
    "カスタムコマンド",
    "スラッシュコマンド",
    "Skills",
    "スキル",
    "Plugins",
    "プラグイン",
    "hooks",
    "フック",
    "frontmatter",
    "フロントマター",
    "Glob",
    "Grep",
    "Plan mode",
    "プランモード",
    "コンテキストウィンドウ",
    "Context Window",
    "トークン",
    "Compacting",
    "Tool Use",
    "Handoff",
    "Headless",
    "Sandbox",
    # フック
    "PreToolUse",
    "PostToolUse",
    "UserPromptSubmit",
    # スラッシュコマンド
    "/init",
    "/compact",
    "/memory",
    "/mcp",
    "/doctor",
)

# =============================================================================
# AI 開発フレームワーク・SDK
# =============================================================================
AI_FRAMEWORKS: tuple[str, ...] = (
    "LangChain",
    "LlamaIndex",
    "Semantic Kernel",
    "LiteLLM",
    "Ollama",
)

# =============================================================================
# サービス（よく言及するもののみ）
# =============================================================================
SERVICES: tuple[str, ...] = (
    "Supabase",
    "Vercel",
    "GitHub",
    "Notion",
    "Obsidian",
)

# =============================================================================
# テスト関連（AI駆動開発文脈で使うもの）
# =============================================================================
TESTING_TERMS: tuple[str, ...] = (
    "pytest",
    "E2E",
    "Happy path",
    "Sad path",
    "Edge case",
    "Unhappy path",
    "Integration test",
    "Unit test",
)

# =============================================================================
# 開発手法・概念（AI駆動開発関連のみ）
# =============================================================================
ARCHITECTURE_TERMS: tuple[str, ...] = (
    "DDD",
    "Onion Architecture",
    "Clean Architecture",
    "Boy Scout Rule",
    "DRY",
    "SOLID",
    "TDD",
    "CI/CD",
    "Vibe Coding",
    "バイブコーディング",
    "AI駆動開発",
    "仕様駆動開発",
    "Spec Driven Development",
    "エージェント型",
    "ハルシネーション",
    "Prompt Engineering",
    "プロンプトエンジニアリング",
    "コンテキストエンジニアリング",
)

# =============================================================================
# フレームワーク（よく言及するもののみ）
# =============================================================================
FRAMEWORKS: tuple[str, ...] = (
    "TypeScript",
    "Python",
    "React",
    "Next.js",
    "Node.js",
    "FastAPI",
    "Tailwind CSS",
    "shadcn/ui",
)

# =============================================================================
# IDE・開発環境（よく言及するもののみ）
# =============================================================================
IDE_TOOLS: tuple[str, ...] = (
    "VS Code",
    "JetBrains",
    "IntelliJ IDEA",
    "PyCharm",
    "WSL",
    "Devcontainer",
    "iTerm2",
    "Docker",
    "Git worktree",
)

# =============================================================================
# とまだ独自
# =============================================================================
TOMADA_TERMS: tuple[str, ...] = (
    "Vibe Coding Studio",
    "とまだ",
)


def build_vocabulary() -> tuple[str, ...]:
    """Combine all vocabulary categories into a single tuple.

    Returns:
        A tuple containing all unique vocabulary terms from all categories.
        Duplicates across categories are removed while preserving order.
    """
    all_terms = (
        AI_SERVICES
        + CODING_TOOLS
        + MCP_TERMS
        + CLAUDE_CODE_TERMS
        + AI_FRAMEWORKS
        + SERVICES
        + TESTING_TERMS
        + ARCHITECTURE_TERMS
        + FRAMEWORKS
        + IDE_TOOLS
        + TOMADA_TERMS
    )
    # dict.fromkeys preserves insertion order and removes duplicates
    return tuple(dict.fromkeys(all_terms))


# Build the default vocabulary from all categories
DEFAULT_VOCABULARY: tuple[str, ...] = build_vocabulary()
