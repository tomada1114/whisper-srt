"""Tests for transcription vocabulary constants."""

import pytest


@pytest.mark.unit
class TestDefaultVocabulary:
    """Tests for DEFAULT_VOCABULARY constant."""

    def test_default_vocabulary_is_tuple(self) -> None:
        """DEFAULT_VOCABULARY should be an immutable tuple."""
        # Arrange & Act
        from transcribe.domain.vocabulary import DEFAULT_VOCABULARY

        # Assert
        assert isinstance(DEFAULT_VOCABULARY, tuple)

    def test_default_vocabulary_is_not_empty(self) -> None:
        """DEFAULT_VOCABULARY should contain vocabulary terms."""
        # Arrange & Act
        from transcribe.domain.vocabulary import DEFAULT_VOCABULARY

        # Assert
        assert len(DEFAULT_VOCABULARY) > 0

    def test_default_vocabulary_contains_ai_terms(self) -> None:
        """DEFAULT_VOCABULARY should contain AI-related terms."""
        # Arrange & Act
        from transcribe.domain.vocabulary import DEFAULT_VOCABULARY

        # Assert
        assert "Claude" in DEFAULT_VOCABULARY
        assert "Claude Code" in DEFAULT_VOCABULARY
        assert "ChatGPT" in DEFAULT_VOCABULARY
        assert "OpenAI" in DEFAULT_VOCABULARY

    def test_default_vocabulary_contains_mcp_terms(self) -> None:
        """DEFAULT_VOCABULARY should contain MCP-related terms."""
        # Arrange & Act
        from transcribe.domain.vocabulary import DEFAULT_VOCABULARY

        # Assert
        assert "MCP" in DEFAULT_VOCABULARY
        assert "Model Context Protocol" in DEFAULT_VOCABULARY

    def test_default_vocabulary_contains_japanese_terms(self) -> None:
        """DEFAULT_VOCABULARY should contain Japanese technical terms."""
        # Arrange & Act
        from transcribe.domain.vocabulary import DEFAULT_VOCABULARY

        # Assert
        # Check for at least some Japanese terms
        japanese_terms = [term for term in DEFAULT_VOCABULARY if any(ord(c) > 127 for c in term)]
        assert len(japanese_terms) > 0

    def test_default_vocabulary_all_strings(self) -> None:
        """All items in DEFAULT_VOCABULARY should be non-empty strings."""
        # Arrange & Act
        from transcribe.domain.vocabulary import DEFAULT_VOCABULARY

        # Assert
        for term in DEFAULT_VOCABULARY:
            assert isinstance(term, str)
            assert len(term) > 0

    def test_default_vocabulary_no_duplicates(self) -> None:
        """DEFAULT_VOCABULARY should not contain duplicate terms."""
        # Arrange & Act
        from transcribe.domain.vocabulary import DEFAULT_VOCABULARY

        # Assert
        assert len(DEFAULT_VOCABULARY) == len(set(DEFAULT_VOCABULARY))
