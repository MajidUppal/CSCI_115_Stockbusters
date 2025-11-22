"""Unit tests for GCS sync functions."""

import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
import os

pytestmark = pytest.mark.unit

# Import after path setup - now handled by conftest.py
rag = pytest.importorskip("rag")
from rag import (
    _get_gcs_client,
    _download_chromadb_from_gcs,
    _upload_chromadb_to_gcs,
    _start_chromadb_server,
    _cleanup_chromadb_server,
)


class TestGetGCSClient:
    """Tests for _get_gcs_client function."""

    def teardown_method(self):
        """Clear mocks after each test."""
        # Removed gc.collect() to save time - let Python handle GC automatically
        pass

    @patch("rag.GCS_AVAILABLE", True)
    @patch("rag.storage")
    @patch("rag.service_account")
    @patch("os.path.exists")
    @patch("os.getenv")
    def test_get_gcs_client_with_key_file(self, mock_getenv, mock_exists, mock_sa, mock_storage):
        """Test GCS client creation with service account key file."""
        # Use spec to limit mock attributes and reduce memory
        mock_getenv.return_value = "/path/to/key.json"
        mock_exists.return_value = True
        mock_creds = Mock(spec=['__class__'])  # Minimal spec
        mock_sa.Credentials.from_service_account_file.return_value = mock_creds
        mock_client = Mock(spec=['bucket', '__class__'])  # Only needed methods
        mock_storage.Client.return_value = mock_client

        result = _get_gcs_client()

        assert result == mock_client
        mock_sa.Credentials.from_service_account_file.assert_called_once_with("/path/to/key.json")
        mock_storage.Client.assert_called_once_with(credentials=mock_creds)

    @patch("rag.GCS_AVAILABLE", True)
    @patch("rag.storage")
    @patch("os.path.exists")
    @patch("os.getenv")
    def test_get_gcs_client_without_key_file(self, mock_getenv, mock_exists, mock_storage):
        """Test GCS client creation without key file (default credentials)."""
        mock_getenv.return_value = "/path/to/key.json"
        mock_exists.return_value = False
        mock_client = Mock(spec=['bucket', '__class__'])  # Minimal spec
        mock_storage.Client.return_value = mock_client

        result = _get_gcs_client()

        assert result == mock_client
        mock_storage.Client.assert_called_once_with()

    @patch("rag.GCS_AVAILABLE", False)
    def test_get_gcs_client_not_available(self):
        """Test GCS client raises error when GCS not available."""
        # rag module already imported via conftest.py path setup

        with pytest.raises(Exception, match="GCS Python client not available"):
            _get_gcs_client()


class TestDownloadChromaDBFromGCS:
    """Tests for _download_chromadb_from_gcs function."""

    def teardown_method(self):
        """Clear mocks after each test."""
        # Removed gc.collect() to save time - let Python handle GC automatically
        pass

    @patch("rag.GCS_AVAILABLE", True)
    @patch("rag._get_gcs_client")
    @patch("os.makedirs")
    @patch("os.path.dirname")
    @patch("rag._touch_chromadb_files")
    def test_download_chromadb_bucket_not_exists(self, mock_touch, mock_dirname, mock_makedirs, mock_get_client):
        """Test download when bucket doesn't exist."""
        # Use minimal mocks with spec to reduce memory
        mock_client = Mock(spec=['bucket'])
        mock_bucket = Mock(spec=['exists', 'list_blobs'])
        mock_bucket.exists.return_value = False
        mock_client.bucket.return_value = mock_bucket
        mock_get_client.return_value = mock_client

        _download_chromadb_from_gcs("test-bucket", "/local/path")

        mock_makedirs.assert_called()
        mock_bucket.list_blobs.assert_not_called()

    @patch("rag.GCS_AVAILABLE", True)
    @patch("rag._get_gcs_client")
    @patch("os.makedirs")
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("rag._touch_chromadb_files")
    def test_download_chromadb_with_blobs(self, mock_touch, mock_dirname, mock_join, mock_makedirs, mock_get_client):
        """Test download with actual blobs - use minimal mocks."""
        # Use spec to limit mock attributes and reduce memory
        mock_client = Mock(spec=['bucket'])
        mock_bucket = Mock(spec=['exists', 'list_blobs'])
        mock_bucket.exists.return_value = True

        # Create minimal mock blob - only needed attributes
        mock_blob = Mock(spec=['name', 'size', 'download_to_filename'])
        mock_blob.name = "chromadb/test_file.txt"
        mock_blob.size = 100  # Small size for memory efficiency
        mock_blob.download_to_filename = Mock()

        # Only one blob to reduce memory
        mock_bucket.list_blobs.return_value = [mock_blob]
        mock_client.bucket.return_value = mock_bucket
        mock_get_client.return_value = mock_client

        mock_join.return_value = "/local/path/test_file.txt"
        mock_dirname.return_value = "/local/path"

        _download_chromadb_from_gcs("test-bucket", "/local/path")

        mock_blob.download_to_filename.assert_called_once()
        mock_touch.assert_called_once_with("/local/path")

    @patch("rag.GCS_AVAILABLE", False)
    def test_download_chromadb_gcs_not_available(self):
        """Test download raises error when GCS not available."""
        # rag module already imported via conftest.py

        with pytest.raises(Exception, match="GCS Python client not available"):
            _download_chromadb_from_gcs("test-bucket", "/local/path")


class TestUploadChromaDBToGCS:
    """Tests for _upload_chromadb_to_gcs function."""

    def teardown_method(self):
        """Clear mocks after each test."""
        # Removed gc.collect() to save time - let Python handle GC automatically
        pass

    @patch("rag.GCS_AVAILABLE", True)
    @patch("rag._get_gcs_client")
    @patch("os.path.exists")
    def test_upload_chromadb_path_not_exists(self, mock_exists, mock_get_client):
        """Test upload when local path doesn't exist."""
        mock_exists.return_value = False

        result = _upload_chromadb_to_gcs("test-bucket", "/nonexistent/path")

        assert result == (0, 0, 0)

    @patch("rag.GCS_AVAILABLE", True)
    @patch("rag._get_gcs_client")
    @patch("os.path.exists")
    @patch("os.walk")
    @patch("builtins.open", new_callable=mock_open, read_data=b"data")  # Smaller data
    @patch("os.path.getsize")
    @patch("hashlib.md5")
    def test_upload_chromadb_with_files(
        self, mock_md5, mock_getsize, mock_file, mock_walk, mock_exists, mock_get_client
    ):
        """Test upload with actual files - reduced to 1 file for memory efficiency."""
        import hashlib

        mock_exists.return_value = True
        # Reduced from 2 files to 1 file to reduce memory
        mock_walk.return_value = [("/local/path", [], ["file1.txt"])]

        # Use spec to limit mock attributes
        mock_client = Mock(spec=['bucket'])
        mock_bucket = Mock(spec=['exists', 'blob'])
        mock_bucket.exists.return_value = True
        mock_blob = Mock(spec=['exists', 'reload', 'md5_hash', 'upload_from_filename'])
        mock_blob.exists.return_value = False
        mock_blob.reload = Mock()
        mock_blob.md5_hash = None
        mock_blob.upload_from_filename = Mock()
        mock_bucket.blob.return_value = mock_blob
        mock_client.bucket.return_value = mock_bucket
        mock_get_client.return_value = mock_client

        mock_getsize.return_value = 10  # Smaller size for memory efficiency
        mock_md5_obj = Mock(spec=['hexdigest'])
        mock_md5_obj.hexdigest.return_value = "abc123"
        mock_md5.return_value = mock_md5_obj

        result = _upload_chromadb_to_gcs("test-bucket", "/local/path")

        assert result[0] > 0  # uploaded_count
        assert mock_blob.upload_from_filename.call_count == 1  # Reduced from 2

    @patch("rag.GCS_AVAILABLE", False)
    def test_upload_chromadb_gcs_not_available(self):
        """Test upload raises error when GCS not available."""
        # rag module already imported via conftest.py

        with pytest.raises(Exception, match="GCS Python client not available"):
            _upload_chromadb_to_gcs("test-bucket", "/local/path")


class TestStartChromaDBServer:
    """Tests for _start_chromadb_server function."""

    def teardown_method(self):
        """Clear mocks after each test."""
        # Removed gc.collect() to save time - let Python handle GC automatically
        pass

    @patch("subprocess.Popen")
    @patch("socket.socket")
    @patch("rag._download_chromadb_from_gcs")
    @patch("os.getenv")
    @patch("os.environ.copy")
    @patch("threading.Thread")  # Mock threading to prevent background threads
    def test_start_chromadb_server_success(self, mock_thread, mock_env_copy, mock_getenv, mock_download, mock_socket, mock_popen):
        """Test successful ChromaDB server start."""
        mock_getenv.return_value = "test-bucket"
        mock_env_copy.return_value = {"CHROMA_TELEMETRY_DISABLED": "1"}
        # Use spec to limit mock attributes
        mock_sock = Mock(spec=['connect_ex', 'close'])
        mock_sock.connect_ex.return_value = 1  # Port not in use
        mock_sock.close = Mock()
        mock_socket.return_value = mock_sock
        
        # Mock process with attributes needed by background threads
        mock_process = Mock()
        mock_process.poll.return_value = None  # Process still running
        mock_process.returncode = None
        mock_process.stdout = Mock()
        mock_process.stdout.readline = Mock(return_value="")  # Empty line to stop iteration
        mock_process.stdout.read = Mock(return_value="")
        mock_popen.return_value = mock_process
        
        # Mock threading to prevent actual background threads from starting
        mock_thread.return_value.start = Mock()

        _start_chromadb_server()

        mock_download.assert_called_once()
        mock_popen.assert_called_once()

    @patch("socket.socket")
    @patch("os.getenv")
    def test_start_chromadb_server_already_running(self, mock_getenv, mock_socket):
        """Test ChromaDB server already running."""
        mock_getenv.return_value = "test-bucket"
        # Use spec to limit mock attributes
        mock_sock = Mock(spec=['connect_ex', 'close'])
        mock_sock.connect_ex.return_value = 0  # Port in use
        mock_sock.close = Mock()
        mock_socket.return_value = mock_sock

        # Should return early without starting
        _start_chromadb_server()

    @patch("os.getenv")
    def test_start_chromadb_server_no_bucket(self, mock_getenv):
        """Test ChromaDB server start without GCS bucket."""
        # rag module already imported via conftest.py
        mock_getenv.return_value = ""

        with pytest.raises(Exception, match="GCS_BUCKET_NAME"):
            _start_chromadb_server()


class TestCleanupChromaDBServer:
    """Tests for _cleanup_chromadb_server function."""

    def teardown_method(self):
        """Clear mocks after each test."""
        # Removed gc.collect() to save time - let Python handle GC automatically
        pass

    @patch("os.getenv")
    @patch("rag._upload_chromadb_to_gcs")
    @patch("rag.GCS_AVAILABLE", False)
    def test_cleanup_chromadb_server_no_process(self, mock_upload, mock_getenv):
        """Test ChromaDB server cleanup when no process exists."""
        # Patch module attributes directly to avoid setup issues
        # Note: @patch with value (False) doesn't create a parameter, only mocks do
        # Parameters are in reverse order of decorators that create mocks (bottom to top)
        with patch.object(rag, '_chromadb_server_process', None), \
             patch.object(rag, '_gcs_synced', False):
            mock_getenv.return_value = "test-bucket"

            # Should not raise error when no process
            _cleanup_chromadb_server()

            # Should not upload if no process was running, GCS not available, or not synced
            mock_upload.assert_not_called()
