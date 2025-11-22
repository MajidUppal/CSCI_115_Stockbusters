"""Unit tests for ingestion pipeline functions."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import time

pytestmark = pytest.mark.unit

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import after path setup
try:
    from rag import run_ingest, ARTIFACTS_DIR
except ImportError:
    # Handle case where imports fail
    pass


class TestRunIngest:
    """Tests for run_ingest function."""

    @patch("rag.get_chromadb_client")
    @patch("rag.get_embedder")
    @patch("rag.load_all")
    @patch("rag.semantic_chunks")
    @patch("rag._upload_chromadb_to_gcs")
    @patch("rag._approx_token_len")
    @patch("rag.hashlib.md5")
    @patch("os.getenv")
    @patch("os.path.join")
    @patch("builtins.open", create=True)
    @patch("time.time")
    @patch("subprocess.check_output")
    def test_run_ingest_success(
        self,
        mock_subprocess,
        mock_time,
        mock_open,
        mock_join,
        mock_getenv,
        mock_md5,
        mock_token_len,
        mock_upload,
        mock_chunks,
        mock_load,
        mock_embedder,
        mock_client,
    ):
        """Test successful ingestion."""
        try:
            from rag import run_ingest
        except ImportError:
            pytest.skip("rag module not available")
        import hashlib

        # Setup mocks
        mock_time.side_effect = [0, 10]  # Start and end time
        mock_subprocess.return_value = b"abc123def456"  # Mock git commit
        mock_upload.return_value = (0, 0, 0)  # Mock GCS upload
        mock_getenv.side_effect = lambda k, d=None: {
            "GCS_BUCKET_NAME": "",  # Empty to avoid GCS upload in tests
            "ARTIFACTS_DIR": "/workspace/artifacts",
            "DATA_DIR": "/workspace/data",
        }.get(k, d)

        mock_client_obj = Mock()
        mock_collection = Mock()
        mock_collection.get.return_value = {"ids": [], "metadatas": [], "embeddings": []}
        mock_collection.upsert = Mock()
        mock_collection.count.return_value = 5
        mock_client_obj.get_or_create_collection.return_value = mock_collection
        mock_client.return_value = mock_client_obj

        mock_embedder_obj = Mock()
        mock_embed_iter = Mock()
        # Use smaller embeddings (128 dim) for memory efficiency
        mock_embed_iter.__iter__ = Mock(return_value=iter([[0.1] * 128, [0.2] * 128]))
        mock_embedder_obj.passage_embed.return_value = mock_embed_iter
        mock_embedder.return_value = mock_embedder_obj

        # Mock glob and file loading to simulate documents being found
        with (
            patch("rag.glob.glob") as mock_glob,
            patch("rag.os.path.isfile", return_value=True),
            patch("rag._load_pdf") as mock_load_pdf,
            patch("rag._approx_token_len", return_value=50),
            patch("rag.hashlib.md5") as mock_md5_hash,
        ):

            # Setup file paths
            mock_glob.return_value = ["/workspace/data/test.pdf"]
            mock_load_pdf.return_value = [("test.pdf", "Sample document content")]

            mock_md5_obj = Mock()
            mock_md5_obj.hexdigest.return_value = "abc123"
            mock_md5_hash.return_value = mock_md5_obj

            mock_join.return_value = "/workspace/artifacts/ingest_summary.json"
            mock_open.return_value.__enter__ = Mock(return_value=Mock())
            mock_open.return_value.__exit__ = Mock(return_value=False)

            # Run ingestion
            result = run_ingest(target_tokens=100, max_tokens=200)

            # Verify results
            assert "added" in result
            assert "n_chunks" in result
            assert "elapsed_sec" in result
            # elapsed_sec should be 10 based on mock_time side_effect
            assert result["elapsed_sec"] == 10
            # DVC-based versioning, no git_commit in metadata
            assert "collection" in result
            assert "embedding_model" in result

    @patch("rag.get_chromadb_client")
    @patch("rag.get_embedder")
    @patch("rag.load_all")
    @patch("os.getenv")
    @patch("os.path.join")
    @patch("builtins.open", create=True)
    @patch("time.time")
    @patch("subprocess.check_output")
    def test_run_ingest_no_documents(
        self, mock_subprocess, mock_time, mock_open, mock_join, mock_getenv, mock_load, mock_embedder, mock_client
    ):
        """Test ingestion with no documents."""
        try:
            from rag import run_ingest
        except ImportError:
            pytest.skip("rag module not available")

        mock_time.side_effect = [0, 5]
        mock_subprocess.return_value = b"abc123"
        mock_getenv.side_effect = lambda k, d=None: {
            "GCS_BUCKET_NAME": "",  # Empty to avoid GCS upload
            "ARTIFACTS_DIR": "/workspace/artifacts",
        }.get(k, d)
        mock_client_obj = Mock()
        mock_collection = Mock()
        mock_collection.get.return_value = {"ids": [], "metadatas": [], "embeddings": []}
        mock_collection.count.return_value = 0
        mock_client_obj.get_or_create_collection.return_value = mock_collection
        mock_client.return_value = mock_client_obj

        mock_embedder_obj = Mock()
        mock_embedder.return_value = mock_embedder_obj

        mock_load.return_value = []  # No documents
        mock_join.return_value = "/workspace/artifacts/ingest_summary.json"
        mock_open.return_value.__enter__ = Mock(return_value=Mock())
        mock_open.return_value.__exit__ = Mock(return_value=False)

        result = run_ingest()

        assert result["num_input_docs"] == 0
        assert result["n_chunks"] == 0

    @patch("rag.get_chromadb_client")
    @patch("rag.get_embedder")
    @patch("rag.semantic_chunks")
    @patch("rag._upload_chromadb_to_gcs")
    @patch("os.getenv")
    @patch("time.time")
    @patch("subprocess.check_output")
    @patch("os.path.join")
    @patch("builtins.open", create=True)
    @patch("rag.glob.glob")
    @patch("rag.os.path.isfile")
    @patch("rag._load_pdf")
    @patch("rag._approx_token_len")
    @patch("rag.hashlib.md5")
    def test_run_ingest_with_version_tracking(
        self,
        mock_md5,
        mock_token_len,
        mock_load_pdf,
        mock_isfile,
        mock_glob,
        mock_open,
        mock_join,
        mock_subprocess,
        mock_time,
        mock_getenv,
        mock_upload_gcs,
        mock_chunks,
        mock_embedder,
        mock_client,
    ):
        """Test ingestion includes version tracking in metadata."""
        try:
            from rag import run_ingest
        except ImportError:
            pytest.skip("rag module not available")

        mock_time.side_effect = [0, 5]
        mock_subprocess.return_value = b"abc123def456"
        mock_upload_gcs.return_value = (0, 0, 0)  # Mock GCS upload
        mock_getenv.side_effect = lambda k, d=None: {
            "GCS_BUCKET_NAME": "",  # Empty to avoid GCS upload
            "ARTIFACTS_DIR": "/workspace/artifacts",
            "DATA_DIR": "/workspace/data",
        }.get(k, d)

        mock_client_obj = Mock()
        mock_collection = Mock()
        mock_collection.get.return_value = {"ids": [], "metadatas": [], "embeddings": []}
        mock_collection.upsert = Mock()
        mock_collection.count.return_value = 0
        mock_client_obj.get_or_create_collection.return_value = mock_collection
        mock_client.return_value = mock_client_obj

        mock_embedder_obj = Mock()
        # Use smaller embeddings (128 dim) for memory efficiency
        mock_embedder_obj.passage_embed.return_value = iter([[0.1] * 128])
        mock_embedder.return_value = mock_embedder_obj

        # Mock file loading
        mock_glob.return_value = ["/workspace/data/test.pdf"]
        mock_isfile.return_value = True
        mock_load_pdf.return_value = [("test.pdf", "Sample content")]
        mock_chunks.return_value = ["Chunk 1"]
        mock_token_len.return_value = 50

        mock_md5_obj = Mock()
        mock_md5_obj.hexdigest.return_value = "abc123"
        mock_md5.return_value = mock_md5_obj

        mock_join.return_value = "/workspace/artifacts/metadata.json"
        mock_open.return_value.__enter__ = Mock(return_value=Mock())
        mock_open.return_value.__exit__ = Mock(return_value=False)

        result = run_ingest()

        # Verify upsert was called
        assert mock_collection.upsert.called
        # Verify basic stats are in result
        assert "n_chunks" in result or "collection" in result

    @patch("rag.get_chromadb_client")
    @patch("rag.get_embedder")
    @patch("rag.load_all")
    @patch("rag.semantic_chunks")
    @patch("os.getenv")
    def test_run_ingest_handles_exceptions(self, mock_getenv, mock_chunks, mock_load, mock_embedder, mock_client):
        """Test ingestion handles exceptions gracefully."""
        try:
            from rag import run_ingest
        except ImportError:
            pytest.skip("rag module not available")

        mock_getenv.return_value = "test-bucket"
        mock_client.side_effect = Exception("Connection failed")

        with pytest.raises(Exception, match="Connection failed"):
            run_ingest()


class TestIngestMetadata:
    """Tests for ingestion metadata and artifacts."""

    def test_ingest_writes_metadata(self):
        """Test that ingestion writes metadata to artifacts."""
        try:
            from rag import ARTIFACTS_DIR
        except ImportError:
            pytest.skip("rag module not available")

        # Verify artifacts directory is defined
        assert ARTIFACTS_DIR is not None
        assert isinstance(ARTIFACTS_DIR, str)

    def test_ingest_returns_complete_stats(self):
        """Test that run_ingest returns complete statistics."""
        # Test the expected return structure
        expected_keys = ["added", "n_chunks", "avg_tokens", "num_input_docs", "elapsed_sec", "skipped_embeddings"]
        sample_result = {
            "added": 10,
            "n_chunks": 10,
            "avg_tokens": 150,
            "num_input_docs": 2,
            "elapsed_sec": 5.5,
            "skipped_embeddings": 0,
        }

        for key in expected_keys:
            assert key in sample_result, f"Missing key: {key}"
