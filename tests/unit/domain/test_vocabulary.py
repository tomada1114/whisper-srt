"""Tests for transcription vocabulary constants."""

import pytest

from transcribe.domain.vocabulary import (
    AI_FRAMEWORKS,
    AI_SERVICES,
    ARCHITECTURE_TERMS,
    CLAUDE_CODE_TERMS,
    CODING_TOOLS,
    DEFAULT_VOCABULARY,
    FRAMEWORKS,
    IDE_TOOLS,
    MCP_TERMS,
    SERVICES,
    TESTING_TERMS,
    TOMADA_TERMS,
    build_vocabulary,
)


@pytest.mark.unit
class TestDefaultVocabulary:
    """Tests for DEFAULT_VOCABULARY constant."""

    def test_default_vocabulary_is_tuple(self) -> None:
        """DEFAULT_VOCABULARY should be an immutable tuple."""
        assert isinstance(DEFAULT_VOCABULARY, tuple)

    def test_default_vocabulary_is_not_empty(self) -> None:
        """DEFAULT_VOCABULARY should contain vocabulary terms."""
        assert len(DEFAULT_VOCABULARY) > 0

    def test_default_vocabulary_contains_ai_terms(self) -> None:
        """DEFAULT_VOCABULARY should contain AI-related terms."""
        assert "Claude" in DEFAULT_VOCABULARY
        assert "Claude Code" in DEFAULT_VOCABULARY
        assert "ChatGPT" in DEFAULT_VOCABULARY
        assert "OpenAI" in DEFAULT_VOCABULARY

    def test_default_vocabulary_contains_mcp_terms(self) -> None:
        """DEFAULT_VOCABULARY should contain MCP-related terms."""
        assert "MCP" in DEFAULT_VOCABULARY
        assert "Model Context Protocol" in DEFAULT_VOCABULARY

    def test_default_vocabulary_contains_japanese_terms(self) -> None:
        """DEFAULT_VOCABULARY should contain Japanese technical terms."""
        japanese_terms = [
            term for term in DEFAULT_VOCABULARY if any(ord(c) > 127 for c in term)
        ]
        assert len(japanese_terms) > 0

    def test_default_vocabulary_all_strings(self) -> None:
        """All items in DEFAULT_VOCABULARY should be non-empty strings."""
        for term in DEFAULT_VOCABULARY:
            assert isinstance(term, str)
            assert len(term) > 0

    def test_default_vocabulary_no_duplicates(self) -> None:
        """DEFAULT_VOCABULARY should not contain duplicate terms."""
        assert len(DEFAULT_VOCABULARY) == len(set(DEFAULT_VOCABULARY))


@pytest.mark.unit
class TestVocabularyCategories:
    """Tests for category-based vocabulary organization."""

    def test_ai_services_category_exists(self) -> None:
        """AI_SERVICES category should exist and be a tuple."""
        assert isinstance(AI_SERVICES, tuple)
        assert "Claude" in AI_SERVICES
        assert "Anthropic" in AI_SERVICES
        assert "OpenAI" in AI_SERVICES

    def test_coding_tools_category_exists(self) -> None:
        """CODING_TOOLS category should exist and be a tuple."""
        assert isinstance(CODING_TOOLS, tuple)
        assert "Cursor" in CODING_TOOLS
        assert "GitHub Copilot" in CODING_TOOLS

    def test_mcp_category_exists(self) -> None:
        """MCP_TERMS category should exist and be a tuple."""
        assert isinstance(MCP_TERMS, tuple)
        assert "MCP" in MCP_TERMS
        assert "Model Context Protocol" in MCP_TERMS
        assert "Playwright MCP" in MCP_TERMS

    def test_claude_code_category_exists(self) -> None:
        """CLAUDE_CODE_TERMS category should exist and be a tuple."""
        assert isinstance(CLAUDE_CODE_TERMS, tuple)
        assert "CLAUDE.md" in CLAUDE_CODE_TERMS
        assert "サブエージェント" in CLAUDE_CODE_TERMS
        assert ".claude/rules" in CLAUDE_CODE_TERMS

    def test_ai_frameworks_category_exists(self) -> None:
        """AI_FRAMEWORKS category should exist and be a tuple."""
        assert isinstance(AI_FRAMEWORKS, tuple)
        assert "LangChain" in AI_FRAMEWORKS
        assert "LlamaIndex" in AI_FRAMEWORKS
        assert "Ollama" in AI_FRAMEWORKS

    def test_frameworks_category_exists(self) -> None:
        """FRAMEWORKS category should exist and be a tuple."""
        assert isinstance(FRAMEWORKS, tuple)
        assert "TypeScript" in FRAMEWORKS
        assert "Next.js" in FRAMEWORKS
        assert "React" in FRAMEWORKS

    def test_services_category_exists(self) -> None:
        """SERVICES category should exist and be a tuple."""
        assert isinstance(SERVICES, tuple)
        assert "Supabase" in SERVICES
        assert "Vercel" in SERVICES

    def test_ide_category_exists(self) -> None:
        """IDE_TOOLS category should exist and be a tuple."""
        assert isinstance(IDE_TOOLS, tuple)
        assert "VS Code" in IDE_TOOLS

    def test_testing_category_exists(self) -> None:
        """TESTING_TERMS category should exist and be a tuple."""
        assert isinstance(TESTING_TERMS, tuple)
        assert "pytest" in TESTING_TERMS
        assert "E2E" in TESTING_TERMS

    def test_architecture_category_exists(self) -> None:
        """ARCHITECTURE_TERMS category should exist and be a tuple."""
        assert isinstance(ARCHITECTURE_TERMS, tuple)
        assert "DDD" in ARCHITECTURE_TERMS
        assert "Onion Architecture" in ARCHITECTURE_TERMS
        assert "CI/CD" in ARCHITECTURE_TERMS

    def test_tomada_terms_category_exists(self) -> None:
        """TOMADA_TERMS category should exist and be a tuple."""
        assert isinstance(TOMADA_TERMS, tuple)
        assert "Vibe Coding Studio" in TOMADA_TERMS
        assert "とまだ" in TOMADA_TERMS

    def test_each_category_has_no_duplicates(self) -> None:
        """Each category should not contain duplicate terms."""
        categories = [
            ("AI_SERVICES", AI_SERVICES),
            ("CODING_TOOLS", CODING_TOOLS),
            ("MCP_TERMS", MCP_TERMS),
            ("CLAUDE_CODE_TERMS", CLAUDE_CODE_TERMS),
            ("AI_FRAMEWORKS", AI_FRAMEWORKS),
            ("FRAMEWORKS", FRAMEWORKS),
            ("SERVICES", SERVICES),
            ("IDE_TOOLS", IDE_TOOLS),
            ("TESTING_TERMS", TESTING_TERMS),
            ("ARCHITECTURE_TERMS", ARCHITECTURE_TERMS),
            ("TOMADA_TERMS", TOMADA_TERMS),
        ]

        for name, category in categories:
            assert len(category) == len(set(category)), f"Duplicates found in {name}"


@pytest.mark.unit
class TestBuildVocabulary:
    """Tests for build_vocabulary function."""

    def test_build_vocabulary_returns_tuple(self) -> None:
        """build_vocabulary should return a tuple."""
        result = build_vocabulary()
        assert isinstance(result, tuple)

    def test_build_vocabulary_combines_all_categories(self) -> None:
        """build_vocabulary should combine all category terms."""
        result = build_vocabulary()

        # All category terms should be in result
        for term in AI_SERVICES:
            assert term in result, f"AI_SERVICES term '{term}' not in result"
        for term in CODING_TOOLS:
            assert term in result, f"CODING_TOOLS term '{term}' not in result"
        for term in MCP_TERMS:
            assert term in result, f"MCP_TERMS term '{term}' not in result"
        for term in CLAUDE_CODE_TERMS:
            assert term in result, f"CLAUDE_CODE_TERMS term '{term}' not in result"
        for term in AI_FRAMEWORKS:
            assert term in result, f"AI_FRAMEWORKS term '{term}' not in result"
        for term in FRAMEWORKS:
            assert term in result, f"FRAMEWORKS term '{term}' not in result"
        for term in SERVICES:
            assert term in result, f"SERVICES term '{term}' not in result"
        for term in IDE_TOOLS:
            assert term in result, f"IDE_TOOLS term '{term}' not in result"
        for term in TESTING_TERMS:
            assert term in result, f"TESTING_TERMS term '{term}' not in result"
        for term in ARCHITECTURE_TERMS:
            assert term in result, f"ARCHITECTURE_TERMS term '{term}' not in result"
        for term in TOMADA_TERMS:
            assert term in result, f"TOMADA_TERMS term '{term}' not in result"

    def test_build_vocabulary_removes_duplicates(self) -> None:
        """build_vocabulary should remove duplicate terms across categories."""
        result = build_vocabulary()
        assert len(result) == len(set(result))

    def test_default_vocabulary_equals_build_vocabulary(self) -> None:
        """DEFAULT_VOCABULARY should equal build_vocabulary result."""
        result = build_vocabulary()
        assert set(DEFAULT_VOCABULARY) == set(result)


@pytest.mark.unit
class TestAIDrivenDevelopmentVocabulary:
    """Tests for AI-driven development focused vocabulary."""

    def test_contains_claude_code_components(self) -> None:
        """Should contain Claude Code component terms."""
        assert "CLAUDE.md" in CLAUDE_CODE_TERMS
        assert "サブエージェント" in CLAUDE_CODE_TERMS
        assert "カスタムコマンド" in CLAUDE_CODE_TERMS
        assert "スキル" in CLAUDE_CODE_TERMS
        assert "frontmatter" in CLAUDE_CODE_TERMS

    def test_contains_claude_code_hooks(self) -> None:
        """Should contain Claude Code hook terms."""
        assert "PreToolUse" in CLAUDE_CODE_TERMS
        assert "PostToolUse" in CLAUDE_CODE_TERMS
        assert "UserPromptSubmit" in CLAUDE_CODE_TERMS

    def test_contains_ai_development_methodology(self) -> None:
        """Should contain AI development methodology terms."""
        assert "Vibe Coding" in ARCHITECTURE_TERMS
        assert "AI駆動開発" in ARCHITECTURE_TERMS
        assert "Prompt Engineering" in ARCHITECTURE_TERMS
        assert "コンテキストエンジニアリング" in ARCHITECTURE_TERMS

    def test_contains_llm_terms(self) -> None:
        """Should contain LLM-related terms."""
        assert "LLM" in AI_SERVICES
        assert "RAG" in AI_SERVICES
        assert "Chain-of-Thought" in AI_SERVICES
        assert "Extended Thinking" in AI_SERVICES

    def test_contains_testing_methodology_terms(self) -> None:
        """Should contain testing methodology terms."""
        assert "Happy path" in TESTING_TERMS
        assert "Sad path" in TESTING_TERMS
        assert "Edge case" in TESTING_TERMS
        assert "Unhappy path" in TESTING_TERMS
