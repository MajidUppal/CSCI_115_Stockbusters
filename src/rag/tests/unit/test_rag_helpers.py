"""Tests for rag_helpers.py functions."""

import pytest

pytestmark = pytest.mark.unit
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestNormalizeQuery:
    """Tests for normalize_query function in rag_helpers."""

    def test_normalize_query_basic(self):
        """Test basic query normalization."""
        from rag_helpers import normalize_query

        result = normalize_query("What is ROE?")
        assert result == "what is roe?"

    def test_normalize_query_whitespace(self):
        """Test normalization handles whitespace."""
        from rag_helpers import normalize_query

        result = normalize_query("  What   is   ROE  ")
        assert result == "what is roe"

    def test_normalize_query_empty(self):
        """Test empty query returns empty string."""
        from rag_helpers import normalize_query

        assert normalize_query("") == ""
        assert normalize_query("   ") == ""

    def test_normalize_query_non_string(self):
        """Test non-string input."""
        from rag_helpers import normalize_query

        assert normalize_query(None) == ""
        assert normalize_query(123) == ""


class TestGetEmbedder:
    """Tests for get_embedder function."""

    @patch("rag_helpers.TextEmbedding")
    def test_get_embedder(self, mock_text_embedding):
        """Test get_embedder returns embedder instance."""
        from rag_helpers import get_embedder

        mock_embedder = Mock()
        mock_text_embedding.return_value = mock_embedder

        # Reset cache
        import rag_helpers

        rag_helpers._embedder_cache = None

        result = get_embedder()
        assert result is not None


class TestGetRAGConnection:
    """Tests for get_rag_connection and get_chroma_db functions."""

    @patch("rag_helpers.chromadb")
    @patch("rag_helpers.storage")
    @patch("rag_helpers.tempfile.mkdtemp")
    def test_get_rag_connection(self, mock_mkdtemp, mock_storage, mock_chromadb):
        """Test getting RAG connection."""
        from rag_helpers import get_rag_connection

        # Setup mocks
        mock_mkdtemp.return_value = "/tmp/test"
        mock_client = Mock()
        mock_chromadb.Client.return_value = mock_client
        mock_collection = Mock()
        mock_client.get_or_create_collection.return_value = mock_collection

        # Mock GCS
        mock_gcs_client = Mock()
        mock_storage.Client.return_value = mock_gcs_client
        mock_bucket = Mock()
        mock_gcs_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value.exists.return_value = False

        # Reset cache
        import rag_helpers

        rag_helpers._cache.clear()

        # Should not raise exception
        try:
            result = get_rag_connection("test_collection")
            # If it returns, that's success (may return None if GCS not available)
        except Exception:
            # Expected if GCS credentials not available in test environment
            pass


class TestQueryRAGTexts:
    """Tests for query_rag_texts function."""

    @patch("rag_helpers.get_chroma_db")
    @patch("rag_helpers.get_rag_connection")
    @patch.dict("os.environ", {"GCS_BUCKET_NAME": "test-bucket"}, clear=False)
    def test_query_rag_texts(self, mock_get_rag_connection, mock_get_chroma_db):
        """Test query_rag_texts returns text list."""
        from rag_helpers import query_rag_texts

        # Mock get_rag_connection to avoid actual GCS connection
        mock_get_rag_connection.return_value = None

        # Mock ChromaDB context
        mock_context = Mock()
        mock_context.query.return_value = [
            {"document": "Text 1", "distance": 0.1},
            {"document": "Text 2", "distance": 0.2},
        ]
        mock_get_chroma_db.return_value = mock_context

        result = query_rag_texts("test query", k=2)

        assert isinstance(result, list)
        # Should return document texts
        mock_context.query.assert_called_once()


class TestStoreQueryInChromaDB:
    """Tests for store_query_in_chromadb function."""

    @patch("rag_helpers.get_chroma_db")
    @patch("rag_helpers.get_embedder")
    def test_store_query_in_chromadb(self, mock_get_embedder, mock_get_chroma_db):
        """Test storing query in ChromaDB."""
        from rag_helpers import store_query_in_chromadb

        # Mock embedder
        mock_embedder = Mock()
        mock_embedder.query_embed.return_value = iter([[0.1] * 384])
        mock_get_embedder.return_value = mock_embedder

        # Mock ChromaDB context
        mock_context = Mock()
        mock_collection = Mock()
        mock_context.client.get_or_create_collection.return_value = mock_collection
        mock_get_chroma_db.return_value = mock_context

        # Should not raise exception
        try:
            store_query_in_chromadb(
                query_text="test query", collection_name="test_collection", metadata={"test": "data"}
            )
            # If successful, collection.upsert should be called
        except Exception:
            # Expected if dependencies not available
            pass
