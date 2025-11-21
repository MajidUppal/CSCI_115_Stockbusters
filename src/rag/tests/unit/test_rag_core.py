"""Unit tests for RAG core functions."""

import pytest

pytestmark = pytest.mark.unit
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import functions to test
from rag import (
    normalize_query,
    _norm,
    _load_txt_md,
    _load_csv,
    load_all,
    semantic_chunks,
    SemanticChunker,
    get_embedder,
    semantic_embed,
    _enrich_chunk_with_context,
    _apply_sentence_overlap,
    _approx_token_len,
)


class TestNormalizeQuery:
    """Tests for normalize_query function."""

    def test_normalize_query_basic(self):
        """Test basic query normalization."""
        result = normalize_query("What is ROE?")
        assert result == "what is roe?"

    def test_normalize_query_with_whitespace(self):
        """Test normalization removes extra whitespace."""
        result = normalize_query("  What   is   ROE?  ")
        assert result == "what is roe?"

    def test_normalize_query_empty(self):
        """Test empty query returns empty string."""
        assert normalize_query("") == ""
        assert normalize_query("   ") == ""

    def test_normalize_query_non_string(self):
        """Test non-string input returns empty string."""
        assert normalize_query(None) == ""
        assert normalize_query(123) == ""
        assert normalize_query([]) == ""


class TestNorm:
    """Tests for _norm text normalization function."""

    def test_norm_basic(self):
        """Test basic text normalization."""
        text = "  Hello   World  "
        result = _norm(text)
        assert result == "Hello World"

    def test_norm_unicode(self):
        """Test unicode normalization."""
        text = "Hello\u2014World"  # Em dash
        result = _norm(text)
        assert "Hello" in result and "World" in result

    def test_norm_empty(self):
        """Test empty text returns empty string."""
        assert _norm("") == ""
        assert _norm(None) == ""

    def test_norm_whitespace(self):
        """Test multiple whitespace normalization."""
        text = "Line 1\n\n\nLine 2"
        result = _norm(text)
        assert "\n\n" in result  # Preserves paragraph breaks
        assert "Line 1" in result and "Line 2" in result


class TestLoadFunctions:
    """Tests for document loading functions."""

    def test_load_txt_md(self, tmp_path):
        """Test loading text/markdown files."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Sample text content")

        result = _load_txt_md(str(test_file))
        assert len(result) == 1
        assert result[0][0] == str(test_file)
        assert "Sample text content" in result[0][1]

    def test_load_csv(self, tmp_path):
        """Test loading CSV files."""
        # Only processes Output_explanation.csv files
        test_file = tmp_path / "Output_explanation.csv"
        test_file.write_text("Feature,Full_Name_or_Formula,Meaning\nROE,Net Income/Equity,Profitability measure")

        result = _load_csv(str(test_file))
        # Should extract text from CSV if it's Output_explanation.csv
        assert isinstance(result, list)

    def test_load_all(self, tmp_path):
        """Test load_all function with multiple files."""
        # Create test files
        (tmp_path / "test1.txt").write_text("Content 1")
        (tmp_path / "test2.txt").write_text("Content 2")

        # Mock to avoid actual file system and PDF issues in CI
        with patch("rag._load_txt_md") as mock_load_txt, patch("rag._load_pdf") as mock_load_pdf, patch(
            "rag._load_csv"
        ) as mock_load_csv:
            mock_load_txt.return_value = [("test1.txt", "Content 1")]
            mock_load_pdf.return_value = []
            mock_load_csv.return_value = []

            result = load_all(str(tmp_path))
            # Should return loaded documents
            assert isinstance(result, list)


class TestSemanticChunking:
    """Tests for semantic chunking functions."""

    @patch("rag.get_embedder")
    @patch("rag.semantic_embed")
    def test_semantic_chunks_small_text(self, mock_embed, mock_get_embedder):
        """Test semantic_chunks with small text that fits in one chunk."""
        small_text = "Short text."
        result = semantic_chunks(small_text, max_tokens=1400)
        assert isinstance(result, list)
        assert len(result) > 0

    @patch("rag.get_embedder")
    @patch("rag.semantic_embed")
    def test_semantic_chunks_large_text(self, mock_embed, mock_get_embedder):
        """Test semantic_chunks with large text that needs splitting."""
        # Create large text
        large_text = " ".join(["Sentence with content."] * 100)

        # Mock embedding to return enough embeddings for all sentences
        # Split by sentences first to estimate how many we need
        sentences = large_text.split(".")
        num_sentences = len([s for s in sentences if s.strip()])
        # Return embeddings for all sentences to avoid IndexError
        mock_embed.return_value = [[0.1] * 384] * max(num_sentences, 100)

        result = semantic_chunks(large_text, max_tokens=100)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_apply_sentence_overlap(self):
        """Test sentence overlap application."""
        chunks = ["First sentence. Second sentence.", "Third sentence. Fourth sentence.", "Fifth sentence."]

        result = _apply_sentence_overlap(chunks, overlap_sentences=1)
        assert len(result) == len(chunks)
        # First chunk should have overlap from second
        assert len(result[0]) >= len(chunks[0])

    def test_apply_sentence_overlap_no_overlap(self):
        """Test sentence overlap with overlap_sentences=0."""
        chunks = ["Chunk 1", "Chunk 2"]
        result = _apply_sentence_overlap(chunks, overlap_sentences=0)
        assert result == chunks

    def test_enrich_chunk_with_context(self):
        """Test chunk context enrichment."""
        chunks = ["First chunk content.", "Second chunk content.", "Third chunk content."]

        result = _enrich_chunk_with_context(chunks, window_size=1)
        assert len(result) == len(chunks)
        # Middle chunk should have context from neighbors
        assert len(result[1]) >= len(chunks[1])

    def test_enrich_chunk_single_chunk(self):
        """Test context enrichment with single chunk."""
        chunks = ["Single chunk"]
        result = _enrich_chunk_with_context(chunks, window_size=2)
        assert result == chunks


class TestEmbeddingFunctions:
    """Tests for embedding functions."""

    @patch("rag.TextEmbedding")
    def test_get_embedder(self, mock_text_embedding):
        """Test get_embedder returns embedder instance."""
        mock_embedder = Mock()
        mock_text_embedding.return_value = mock_embedder

        # Reset global cache
        import rag

        rag._EMBEDDER = None

        result = get_embedder()
        assert result is not None

    @patch("rag.get_embedder")
    def test_semantic_embed(self, mock_get_embedder):
        """Test semantic_embed function."""
        mock_embedder = Mock()
        mock_embedder.embed.return_value = iter([[0.1] * 384, [0.2] * 384])
        mock_get_embedder.return_value = mock_embedder

        texts = ["text1", "text2"]
        result = semantic_embed(texts)

        assert isinstance(result, list)
        assert len(result) == len(texts)


class TestUtilityFunctions:
    """Tests for utility functions."""

    def test_approx_token_len(self):
        """Test token length approximation."""
        text = "This is a test sentence with multiple words."
        result = _approx_token_len(text)
        assert isinstance(result, int)
        assert result > 0

    def test_approx_token_len_short(self):
        """Test token length for short text."""
        result = _approx_token_len("Hi")
        assert result >= 1

    def test_approx_token_len_empty(self):
        """Test token length for empty text."""
        result = _approx_token_len("")
        assert result >= 1  # Should return at least 1


class TestSemanticChunker:
    """Tests for SemanticChunker class."""

    def test_semantic_chunker_init(self):
        """Test SemanticChunker initialization."""
        mock_embed_func = Mock(return_value=[[0.1] * 384])

        chunker = SemanticChunker(
            embedding_function=mock_embed_func,
            buffer_size=1,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95.0,
        )

        assert chunker is not None
        assert chunker.buffer_size == 1
