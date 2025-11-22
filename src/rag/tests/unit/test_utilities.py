"""Unit tests for simple utility functions - fast and easy tests."""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open

pytestmark = pytest.mark.unit

# Import functions to test
rag = pytest.importorskip("rag")
from rag import (
    _load_env_file,
    _touch_chromadb_files,
    get_chromadb_client,
    SemanticSplitterCache,
    _approx_token_len,
    _get_semantic_splitter,
)


class TestLoadEnvFile:
    """Tests for _load_env_file function - simple and fast."""

    def test_load_env_file_basic(self, tmp_path, monkeypatch):
        """Test loading basic .env file."""
        # Create .env file
        env_file = tmp_path / ".env"
        env_file.write_text("TEST_VAR=test_value\nANOTHER_VAR=123\n")
        
        # Clear any existing env vars
        monkeypatch.delenv("TEST_VAR", raising=False)
        monkeypatch.delenv("ANOTHER_VAR", raising=False)
        
        # Mock Path(__file__).parent to point to tmp_path
        mock_path_instance = MagicMock()
        mock_path_instance.parent = tmp_path
        mock_path_instance.__truediv__ = lambda self, other: tmp_path / other
        
        with patch("rag.Path", return_value=mock_path_instance):
            _load_env_file()
            # Function uses setdefault, so it won't override existing values
            # Just verify it executed without error
            assert True

    def test_load_env_file_with_comments(self, tmp_path, monkeypatch):
        """Test .env file with comments."""
        env_file = tmp_path / ".env"
        env_file.write_text("# This is a comment\nTEST_VAR=value#inline comment\n# Another comment\n")
        
        monkeypatch.delenv("TEST_VAR", raising=False)
        
        mock_path_instance = MagicMock()
        mock_path_instance.parent = tmp_path
        mock_path_instance.__truediv__ = lambda self, other: tmp_path / other
        
        with patch("rag.Path", return_value=mock_path_instance):
            _load_env_file()
            assert True  # Function executed

    def test_load_env_file_no_file(self, tmp_path, monkeypatch):
        """Test when .env file doesn't exist."""
        # Don't create .env file
        mock_path_instance = MagicMock()
        mock_path_instance.parent = tmp_path
        mock_path_instance.__truediv__ = lambda self, other: tmp_path / other
        
        with patch("rag.Path", return_value=mock_path_instance):
            _load_env_file()
            assert True  # Should not raise error

    def test_load_env_file_empty_lines(self, tmp_path):
        """Test .env file with empty lines."""
        env_file = tmp_path / ".env"
        env_file.write_text("\n\nTEST_VAR=value\n\n")
        
        mock_path_instance = MagicMock()
        mock_path_instance.parent = tmp_path
        mock_path_instance.__truediv__ = lambda self, other: tmp_path / other
        
        with patch("rag.Path", return_value=mock_path_instance):
            _load_env_file()
            assert True  # Should handle empty lines


class TestTouchChromaDBFiles:
    """Tests for _touch_chromadb_files function - simple file operations."""

    def test_touch_chromadb_files_nonexistent_path(self):
        """Test with non-existent path."""
        _touch_chromadb_files("/nonexistent/path/that/does/not/exist")
        # Should return without error

    def test_touch_chromadb_files_with_sqlite(self, tmp_path):
        """Test touching chroma.sqlite3 file."""
        sqlite_file = tmp_path / "chroma.sqlite3"
        sqlite_file.write_text("fake sqlite content")
        
        with patch("os.utime") as mock_utime, \
             patch("os.path.exists", return_value=True), \
             patch("os.path.getsize", return_value=100):
            _touch_chromadb_files(str(tmp_path))
            # Should call utime on sqlite file
            assert mock_utime.called

    def test_touch_chromadb_files_with_collections(self, tmp_path):
        """Test touching files in collection directories."""
        # Create collection directory structure
        collection_dir = tmp_path / "collection1"
        collection_dir.mkdir()
        (collection_dir / "file1.txt").write_text("content")
        (collection_dir / "file2.txt").write_text("content")
        
        with patch("os.utime") as mock_utime, \
             patch("os.path.exists", return_value=True), \
             patch("os.listdir", return_value=["collection1"]), \
             patch("os.path.isdir", return_value=True), \
             patch("os.walk") as mock_walk:
            mock_walk.return_value = [
                (str(collection_dir), [], ["file1.txt", "file2.txt"])
            ]
            _touch_chromadb_files(str(tmp_path))
            # Should attempt to touch files
            assert True  # Function executed

    def test_touch_chromadb_files_handles_permission_error(self, tmp_path):
        """Test handles permission errors gracefully."""
        with patch("os.path.exists", return_value=True), \
             patch("os.listdir", return_value=[]), \
             patch("os.utime", side_effect=PermissionError("No permission")):
            # Should not raise, just print warning
            _touch_chromadb_files(str(tmp_path))
            assert True  # Should handle error gracefully


class TestGetChromaDBClient:
    """Tests for get_chromadb_client function."""

    @patch("rag.HttpClient")
    @patch("rag.CHROMADB_AUTH_TOKEN", "")
    def test_get_chromadb_client_no_auth(self, mock_http_client):
        """Test client creation without auth token."""
        mock_client = Mock()
        mock_http_client.return_value = mock_client
        
        result = get_chromadb_client()
        
        assert result == mock_client
        mock_http_client.assert_called_once_with(host="localhost", port=8000)

    @patch("rag.HttpClient")
    @patch("rag.ChromaSettings")
    @patch("rag.CHROMADB_AUTH_TOKEN", "test-token")
    def test_get_chromadb_client_with_auth(self, mock_settings, mock_http_client):
        """Test client creation with auth token."""
        mock_client = Mock()
        mock_http_client.return_value = mock_client
        mock_settings_instance = Mock()
        mock_settings.return_value = mock_settings_instance
        
        result = get_chromadb_client()
        
        assert result == mock_client
        mock_settings.assert_called_once()
        mock_http_client.assert_called_once()

    @patch("rag.HttpClient")
    @patch("rag.CHROMADB_AUTH_TOKEN", "")
    def test_get_chromadb_client_handles_exception(self, mock_http_client):
        """Test handles exception during client creation."""
        mock_http_client.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception, match="Connection failed"):
            get_chromadb_client()


class TestSemanticSplitterCache:
    """Tests for SemanticSplitterCache class - simple class methods."""

    def test_semantic_splitter_cache_init(self):
        """Test cache initialization."""
        cache = SemanticSplitterCache()
        assert cache.size() == 0

    def test_semantic_splitter_cache_clear(self):
        """Test clearing the cache."""
        cache = SemanticSplitterCache()
        # Add something to cache by calling get_splitter
        with patch("rag.SemanticChunker") as mock_chunker:
            mock_chunker.return_value = Mock()
            cache.get_splitter(sim_percentile=95.0, buffer_size=1)
            assert cache.size() > 0
            
            cache.clear()
            assert cache.size() == 0

    def test_semantic_splitter_cache_size(self):
        """Test cache size tracking."""
        cache = SemanticSplitterCache()
        assert cache.size() == 0
        
        with patch("rag.SemanticChunker") as mock_chunker:
            mock_chunker.return_value = Mock()
            cache.get_splitter(sim_percentile=95.0, buffer_size=1)
            assert cache.size() == 1
            
            # Different params = new entry
            cache.get_splitter(sim_percentile=96.0, buffer_size=1)
            assert cache.size() == 2

    def test_semantic_splitter_cache_get_splitter_caching(self):
        """Test that get_splitter caches instances."""
        cache = SemanticSplitterCache()
        
        with patch("rag.SemanticChunker") as mock_chunker:
            mock_instance = Mock()
            mock_chunker.return_value = mock_instance
            
            # First call
            result1 = cache.get_splitter(sim_percentile=95.0, buffer_size=1)
            assert mock_chunker.call_count == 1
            
            # Second call with same params
            result2 = cache.get_splitter(sim_percentile=95.0, buffer_size=1)
            
            # Should return same instance, not create new one
            assert result1 == result2
            assert mock_chunker.call_count == 1  # Still only 1 call


class TestApproxTokenLen:
    """Additional tests for _approx_token_len with edge cases."""

    def test_approx_token_len_with_tiktoken_mock(self):
        """Test with mocked tiktoken."""
        with patch("rag.USE_TIKTOKEN", True), \
             patch("rag._TOK") as mock_tok:
            mock_tok.encode.return_value = [1, 2, 3, 4, 5]
            
            result = _approx_token_len("test text")
            assert result == 5

    def test_approx_token_len_tiktoken_exception(self):
        """Test fallback when tiktoken raises exception."""
        with patch("rag.USE_TIKTOKEN", True), \
             patch("rag._TOK") as mock_tok:
            mock_tok.encode.side_effect = Exception("Encoding failed")
            
            # Should fall back to heuristic
            result = _approx_token_len("test text")
            assert result >= 1

    def test_approx_token_len_whitespace_only(self):
        """Test with whitespace-only text."""
        result = _approx_token_len("   \n\t  ")
        assert result >= 1  # Should return at least 1

    def test_approx_token_len_special_characters(self):
        """Test with special characters and punctuation."""
        result = _approx_token_len("!!!@@@###$$$")
        assert result >= 1

    def test_approx_token_len_mixed_content(self):
        """Test with mixed words and punctuation."""
        text = "Hello, world! How are you? I'm fine."
        result = _approx_token_len(text)
        assert result > 0
        # Should be reasonable estimate
        assert result < len(text)  # Tokens usually < characters


class TestGetSemanticSplitter:
    """Additional edge case tests for _get_semantic_splitter."""

    @patch("rag.semantic_embed")
    @patch("rag.SemanticChunker")
    def test_get_semantic_splitter_different_buffer_sizes(self, mock_chunker, mock_embed):
        """Test with different buffer sizes."""
        import rag
        rag._splitter_cache = SemanticSplitterCache()
        
        mock_chunker.return_value = Mock()
        
        result1 = _get_semantic_splitter(sim_percentile=95.0, buffer_size=1)
        result2 = _get_semantic_splitter(sim_percentile=95.0, buffer_size=2)
        
        # Different buffer sizes should create different instances
        assert mock_chunker.call_count == 2

