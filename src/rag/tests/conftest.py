"""Pytest fixtures for RAG tests."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from typing import List, Dict, Any
import numpy as np


@pytest.fixture
def mock_chromadb_client():
    """Mock ChromaDB HTTP client."""
    client = Mock()
    collection = Mock()

    # Mock collection methods
    collection.count.return_value = 100
    collection.metadata = {"hnsw:space": "cosine"}
    collection.query.return_value = {
        "ids": [["doc1", "doc2"]],
        "documents": [["Sample document text 1", "Sample document text 2"]],
        "metadatas": [[{"source": "test.pdf", "page": 1}, {"source": "test.pdf", "page": 2}]],
        "distances": [[0.1, 0.2]],
    }
    collection.get_or_create_collection.return_value = collection
    client.get_or_create_collection.return_value = collection

    return client, collection


@pytest.fixture
def mock_embedder():
    """Mock FastEmbed embedder."""
    embedder = Mock()

    # Mock embedding generation
    def mock_embed(texts, **kwargs):
        # Return mock embeddings (384 dim for BGE-small)
        embeddings = []
        for text in texts:
            # Generate deterministic mock embedding
            emb = np.random.RandomState(hash(text) % 2**32).randn(384).astype(np.float32)
            embeddings.append(emb.tolist())
        return iter(embeddings)

    def mock_query_embed(text):
        # Single query embedding
        emb = np.random.RandomState(hash(text) % 2**32).randn(384).astype(np.float32)
        return iter([emb.tolist()])

    embedder.embed = mock_embed
    embedder.query_embed = mock_query_embed

    return embedder


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "This is a sample document for testing. It contains multiple sentences. Each sentence has some content."


@pytest.fixture
def sample_chunks():
    """Sample text chunks for testing."""
    return [
        "First chunk of text with some content.",
        "Second chunk with different content.",
        "Third chunk with more text.",
    ]


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        ("test1.pdf", "Document 1 content about finance and stocks."),
        ("test2.pdf", "Document 2 content about investment strategies."),
        ("test3.txt", "Document 3 plain text content."),
    ]


@pytest.fixture
def mock_fastapi_app():
    """Mock FastAPI app for testing."""
    from fastapi.testclient import TestClient
    import sys
    from pathlib import Path

    # Add parent directory to path to import rag
    sys.path.insert(0, str(Path(__file__).parent.parent))

    # Patch ChromaDB and GCS dependencies before importing
    with patch("rag.get_chromadb_client"), patch("rag._get_gcs_client"), patch("rag._start_chromadb_server"):
        from rag import make_app

        app = make_app()
        return TestClient(app)


@pytest.fixture
def temp_data_dir(tmp_path):
    """Temporary data directory for testing."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return str(data_dir)


@pytest.fixture
def sample_query_results():
    """Sample query results from ChromaDB."""
    return [
        {
            "rank": 1,
            "id": "doc1",
            "text": "Return on Equity (ROE) measures profitability.",
            "metadata": {"source": "finance.pdf", "page": 42},
            "distance": 0.15,
        },
        {
            "rank": 2,
            "id": "doc2",
            "text": "ROE is calculated as Net Income divided by Equity.",
            "metadata": {"source": "accounting.pdf", "page": 15},
            "distance": 0.28,
        },
    ]
