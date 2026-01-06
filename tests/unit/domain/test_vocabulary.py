"""Tests for transcription vocabulary constants."""

import pytest

from transcribe.domain.vocabulary import DEFAULT_VOCABULARY


@pytest.mark.unit
class TestDefaultVocabulary:
    """Tests for DEFAULT_VOCABULARY constant."""

    def test_default_vocabulary_is_tuple(self) -> None:
        """DEFAULT_VOCABULARY should be an immutable tuple."""
        assert isinstance(DEFAULT_VOCABULARY, tuple)

    def test_default_vocabulary_is_empty(self) -> None:
        """DEFAULT_VOCABULARY should be empty by default."""
        assert DEFAULT_VOCABULARY == ()
