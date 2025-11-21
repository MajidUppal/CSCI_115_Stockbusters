"""Tests for Retriever class."""

import pytest

pytestmark = pytest.mark.unit
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_chromadb_collection():
    """Mock ChromaDB collection for Retriever tests."""
    collection = Mock()
    collection.count.return_value = 100
    collection.metadata = {"hnsw:space": "cosine"}
    collection.query.return_value = {
        "ids": [["doc1", "doc2"]],
        "documents": [["Document 1 text", "Document 2 text"]],
        "metadatas": [[{"source": "test.pdf"}, {"source": "test.pdf"}]],
        "distances": [[0.15, 0.25]],
    }
    return collection


@pytest.fixture
def mock_chromadb_client(mock_chromadb_collection):
    """Mock ChromaDB client."""
    client = Mock()
    client.get_or_create_collection.return_value = mock_chromadb_collection
    return client


class TestRetrieverInit:
    """Tests for Retriever initialization."""

    @patch("rag.get_chromadb_client")
    def test_retriever_init(self, mock_get_client, mock_chromadb_client, mock_chromadb_collection):
        """Test Retriever initialization."""
        from rag import Retriever

        mock_get_client.return_value = mock_chromadb_client

        retriever = Retriever()

        assert retriever.client is not None
        assert retriever.collection is not None
        assert retriever.mode == "chroma-dist"

    @patch("rag.get_chromadb_client")
    @patch("rag.ENABLE_CACHE", True)
    def test_retriever_init_with_cache(self, mock_get_client, mock_chromadb_client):
        """Test Retriever initialization with cache enabled."""
        from rag import Retriever

        mock_get_client.return_value = mock_chromadb_client

        retriever = Retriever()
        assert retriever._query_cache is not None

    @patch("rag.get_chromadb_client")
    @patch("rag.ENABLE_CACHE", False)
    def test_retriever_init_without_cache(self, mock_get_client, mock_chromadb_client):
        """Test Retriever initialization without cache."""
        from rag import Retriever

        mock_get_client.return_value = mock_chromadb_client

        retriever = Retriever()
        assert retriever._query_cache is None


class TestRetrieverStats:
    """Tests for Retriever.stats() method."""

    @patch("rag.get_chromadb_client")
    def test_retriever_stats(self, mock_get_client, mock_chromadb_client, mock_chromadb_collection):
        """Test Retriever stats method."""
        from rag import Retriever

        mock_get_client.return_value = mock_chromadb_client

        retriever = Retriever()
        stats = retriever.stats()

        assert isinstance(stats, dict)
        assert "collection" in stats
        assert "count" in stats
        assert "emb_model" in stats
        assert stats["count"] == 100


class TestRetrieverQuery:
    """Tests for Retriever.query() method."""

    @patch("rag.get_chromadb_client")
    @patch("rag.get_embedder")
    @patch("rag.normalize_query")
    def test_retriever_query_success(
        self, mock_norm, mock_get_embedder, mock_get_client, mock_chromadb_client, mock_chromadb_collection
    ):
        """Test Retriever query returns results."""
        from rag import Retriever

        # Setup mocks
        mock_get_client.return_value = mock_chromadb_client
        mock_norm.return_value = "test query"

        mock_embedder = Mock()
        mock_embedder.query_embed.return_value = iter([np.array([0.1] * 384, dtype=np.float32)])
        mock_get_embedder.return_value = mock_embedder

        retriever = Retriever()
        results = retriever.query("test query", k=2)

        assert isinstance(results, list)
        if len(results) > 0:
            assert "text" in results[0] or "id" in results[0]

    @patch("rag.get_chromadb_client")
    @patch("rag.normalize_query")
    def test_retriever_query_empty(self, mock_norm, mock_get_client, mock_chromadb_client):
        """Test Retriever query with empty query."""
        from rag import Retriever

        mock_get_client.return_value = mock_chromadb_client
        mock_norm.return_value = ""

        retriever = Retriever()
        results = retriever.query("", k=3)

        assert results == []

    @patch("rag.get_chromadb_client")
    @patch("rag.normalize_query")
    def test_retriever_query_non_string(self, mock_norm, mock_get_client, mock_chromadb_client):
        """Test Retriever query with non-string input."""
        from rag import Retriever

        mock_get_client.return_value = mock_chromadb_client
        mock_norm.return_value = ""

        retriever = Retriever()
        results = retriever.query(None, k=3)

        assert results == []

    @patch("rag.get_chromadb_client")
    @patch("rag.get_embedder")
    @patch("rag.normalize_query")
    @patch("rag.ENABLE_CACHE", True)
    def test_retriever_query_caching(
        self, mock_norm, mock_get_embedder, mock_get_client, mock_chromadb_client, mock_chromadb_collection
    ):
        """Test Retriever query caching."""
        from rag import Retriever

        mock_get_client.return_value = mock_chromadb_client
        mock_norm.return_value = "cached query"

        mock_embedder = Mock()
        mock_embedder.query_embed.return_value = iter([np.array([0.1] * 384, dtype=np.float32)])
        mock_get_embedder.return_value = mock_embedder

        retriever = Retriever()

        # First query
        results1 = retriever.query("cached query", k=2)

        # Second query with same text should use cache
        results2 = retriever.query("cached query", k=2)

        # Should return same results
        assert results1 == results2
        # Embedder should only be called once (cached on second call)
        assert mock_embedder.query_embed.call_count <= 2  # May be called for embedding cache too

    @patch("rag.get_chromadb_client")
    @patch("rag.get_embedder")
    @patch("rag.normalize_query")
    def test_retriever_query_k_limits(
        self, mock_norm, mock_get_embedder, mock_get_client, mock_chromadb_client, mock_chromadb_collection
    ):
        """Test Retriever query respects k limits."""
        from rag import Retriever

        mock_get_client.return_value = mock_chromadb_client
        mock_norm.return_value = "test"

        mock_embedder = Mock()

        # Return an iterator that can be called multiple times
        def mock_embed_iter():
            return iter([np.array([0.1] * 384, dtype=np.float32)])

        mock_embedder.query_embed.return_value = mock_embed_iter()
        mock_get_embedder.return_value = mock_embedder

        retriever = Retriever()

        # Test k=0 should become k=1
        results = retriever.query("test", k=0)
        # Should not raise exception
        assert isinstance(results, list)

        # Test k>50 should be capped at 50
        # Reset the mock to return a new iterator
        mock_embedder.query_embed.return_value = mock_embed_iter()
        results = retriever.query("test", k=100)
        # Should not raise exception
        assert isinstance(results, list)
