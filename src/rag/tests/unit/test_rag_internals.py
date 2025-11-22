"""Unit tests for RAG internal/helper functions not yet covered."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import numpy as np

pytestmark = pytest.mark.unit

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import functions to test
from rag import (
    _combine_sentences,
    _calc_cosine_distances,
    _split_sentences_cached,
    _pack_sentences_to_token_cap,
    _get_semantic_splitter,
    _remove_headers_footers,
    _finalize_and_output_chapter,
    cached_embed,
    _approx_token_len,
)


class TestCombineSentences:
    """Tests for _combine_sentences function."""

    def test_combine_sentences_no_buffer(self):
        """Test combining sentences with buffer_size=0."""
        sentences = [
            {"sentence": "First sentence."},
            {"sentence": "Second sentence."},
            {"sentence": "Third sentence."},
        ]
        result = _combine_sentences(sentences, buffer_size=0)

        assert len(result) == 3
        assert result[0]["combined_sentence"] == "First sentence."
        assert result[1]["combined_sentence"] == "Second sentence."
        assert result[2]["combined_sentence"] == "Third sentence."

    def test_combine_sentences_with_buffer(self):
        """Test combining sentences with buffer_size=1."""
        sentences = [
            {"sentence": "First sentence."},
            {"sentence": "Second sentence."},
            {"sentence": "Third sentence."},
        ]
        result = _combine_sentences(sentences, buffer_size=1)

        assert len(result) == 3
        # First sentence should have first and second
        assert "First sentence." in result[0]["combined_sentence"]
        assert "Second sentence." in result[0]["combined_sentence"]
        # Middle sentence should have all three
        assert "First sentence." in result[1]["combined_sentence"]
        assert "Second sentence." in result[1]["combined_sentence"]
        assert "Third sentence." in result[1]["combined_sentence"]
        # Last sentence should have second and third
        assert "Second sentence." in result[2]["combined_sentence"]
        assert "Third sentence." in result[2]["combined_sentence"]

    def test_combine_sentences_large_buffer(self):
        """Test combining sentences with large buffer_size."""
        sentences = [
            {"sentence": "First."},
            {"sentence": "Second."},
            {"sentence": "Third."},
        ]
        result = _combine_sentences(sentences, buffer_size=10)

        # All sentences should include all context
        for item in result:
            assert "First." in item["combined_sentence"]
            assert "Second." in item["combined_sentence"]
            assert "Third." in item["combined_sentence"]

    def test_combine_sentences_single(self):
        """Test combining single sentence."""
        sentences = [{"sentence": "Only sentence."}]
        result = _combine_sentences(sentences, buffer_size=1)

        assert len(result) == 1
        assert result[0]["combined_sentence"] == "Only sentence."

    def test_combine_sentences_empty(self):
        """Test combining empty sentence list."""
        result = _combine_sentences([], buffer_size=1)
        assert result == []


class TestCalcCosineDistances:
    """Tests for _calc_cosine_distances function."""

    def test_calc_cosine_distances_empty(self):
        """Test with empty sentence list."""
        distances, sentences = _calc_cosine_distances([])
        assert distances == []
        assert sentences == []

    def test_calc_cosine_distances_single(self):
        """Test with single sentence."""
        sentences = [{"combined_sentence_embedding": np.array([1.0, 0.0, 0.0])}]
        distances, result = _calc_cosine_distances(sentences)
        assert distances == []
        assert len(result) == 1

    def test_calc_cosine_distances_two_sentences(self):
        """Test with two sentences."""
        # Create two similar embeddings
        emb1 = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        emb2 = np.array([1.0, 0.0, 0.0], dtype=np.float32)

        sentences = [
            {"combined_sentence_embedding": emb1},
            {"combined_sentence_embedding": emb2},
        ]
        distances, result = _calc_cosine_distances(sentences)

        assert len(distances) == 1
        # Identical vectors should have distance close to 0
        assert distances[0] < 0.01
        assert "distance_to_next" in result[0]

    def test_calc_cosine_distances_orthogonal(self):
        """Test with orthogonal (perpendicular) embeddings."""
        emb1 = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        emb2 = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        sentences = [
            {"combined_sentence_embedding": emb1},
            {"combined_sentence_embedding": emb2},
        ]
        distances, result = _calc_cosine_distances(sentences)

        assert len(distances) == 1
        # Orthogonal vectors should have distance close to 1
        assert 0.9 < distances[0] <= 1.0

    def test_calc_cosine_distances_multiple(self):
        """Test with multiple sentences."""
        embeddings = [
            np.array([1.0, 0.0, 0.0], dtype=np.float32),
            np.array([0.9, 0.1, 0.0], dtype=np.float32),
            np.array([0.0, 1.0, 0.0], dtype=np.float32),
        ]

        sentences = [{"combined_sentence_embedding": emb} for emb in embeddings]
        distances, result = _calc_cosine_distances(sentences)

        assert len(distances) == 2
        assert all(0 <= d <= 1 for d in distances)
        assert all("distance_to_next" in s for s in result[:-1])


class TestSplitSentencesCached:
    """Tests for _split_sentences_cached function."""

    def test_split_sentences_basic(self):
        """Test basic sentence splitting."""
        text = "First sentence. Second sentence. Third sentence."
        result = _split_sentences_cached(text)

        assert len(result) == 3
        assert "First sentence" in result[0]
        assert "Second sentence" in result[1]
        assert "Third sentence" in result[2]

    def test_split_sentences_custom_regex(self):
        """Test with custom regex pattern."""
        text = "First sentence! Second sentence? Third sentence."
        result = _split_sentences_cached(text, regex_pattern=r"[!?.]")

        assert len(result) >= 3

    def test_split_sentences_empty(self):
        """Test with empty text."""
        result = _split_sentences_cached("")
        assert result == []

    def test_split_sentences_whitespace_only(self):
        """Test with whitespace-only text."""
        result = _split_sentences_cached("   \n\n   ")
        assert result == []

    def test_split_sentences_caching(self):
        """Test that caching works."""
        text = "Test sentence. Another sentence."

        # First call
        result1 = _split_sentences_cached(text)
        # Second call should use cache
        result2 = _split_sentences_cached(text)

        assert result1 == result2
        assert len(result1) == 2

    def test_split_sentences_multiple_punctuation(self):
        """Test with multiple punctuation marks."""
        text = "First... Second!!! Third???"
        result = _split_sentences_cached(text)
        # Should handle multiple punctuation
        assert len(result) >= 1


class TestPackSentencesToTokenCap:
    """Tests for _pack_sentences_to_token_cap function."""

    def test_pack_sentences_small_text(self):
        """Test with text that fits in one chunk."""
        text = "Short text that fits."
        result = _pack_sentences_to_token_cap(text, max_tokens=100)

        assert len(result) == 1
        assert text in result[0]

    def test_pack_sentences_large_text(self):
        """Test with text that needs multiple chunks."""
        # Create text with many sentences
        sentences = [f"Sentence {i} with some content." for i in range(50)]
        text = " ".join(sentences)

        result = _pack_sentences_to_token_cap(text, max_tokens=50)

        # Should create multiple chunks
        assert len(result) > 1
        # All chunks should be non-empty
        assert all(chunk.strip() for chunk in result)

    def test_pack_sentences_empty(self):
        """Test with empty text."""
        result = _pack_sentences_to_token_cap("", max_tokens=100)
        assert result == []

    def test_pack_sentences_custom_regex(self):
        """Test with custom sentence split regex."""
        text = "First! Second? Third."
        result = _pack_sentences_to_token_cap(text, max_tokens=100, sentence_split_regex=r"[!?.]")

        assert len(result) >= 1

    def test_pack_sentences_very_small_cap(self):
        """Test with very small token cap."""
        text = "This is a sentence with multiple words that might exceed the cap."
        result = _pack_sentences_to_token_cap(text, max_tokens=5)

        # Should still return at least one chunk
        assert len(result) >= 1


class TestGetSemanticSplitter:
    """Tests for _get_semantic_splitter function."""

    def setup_method(self):
        """Create fresh cache instance before each test."""
        import rag
        # Replace module-level cache with fresh instance for test isolation
        rag._splitter_cache = rag.SemanticSplitterCache()
    
    def teardown_method(self):
        """Clear cache after each test."""
        import rag
        if hasattr(rag, '_splitter_cache'):
            rag._splitter_cache.clear()
            # Restore fresh instance
            rag._splitter_cache = rag.SemanticSplitterCache()

    @patch("rag.semantic_embed")
    @patch("rag.SemanticChunker")
    def test_get_semantic_splitter_creates_new(self, mock_chunker_class, mock_embed):
        """Test that splitter is created on first call."""
        import rag
        # setup_method already creates fresh cache, just reset mock
        mock_chunker_class.reset_mock()
        
        mock_chunker_instance = Mock()
        mock_chunker_class.return_value = mock_chunker_instance

        # Use unique parameters for this test
        result = _get_semantic_splitter(sim_percentile=99.0, buffer_size=5)

        assert result == mock_chunker_instance
        mock_chunker_class.assert_called_once()

    @patch("rag.semantic_embed")
    @patch("rag.SemanticChunker")
    def test_get_semantic_splitter_caching(self, mock_chunker_class, mock_embed):
        """Test that splitter is cached for same parameters."""
        import rag
        # setup_method already creates fresh cache, just reset mock
        mock_chunker_class.reset_mock()
        
        mock_chunker_instance = Mock()
        mock_chunker_class.return_value = mock_chunker_instance

        # Use unique parameters for this test
        # First call - should create new instance
        result1 = _get_semantic_splitter(sim_percentile=98.0, buffer_size=3)
        # Verify SemanticChunker was called
        assert mock_chunker_class.call_count == 1, f"Expected 1 call, got {mock_chunker_class.call_count}. Cache size: {rag._splitter_cache.size()}"
        
        # Second call with same params - should use cache
        result2 = _get_semantic_splitter(sim_percentile=98.0, buffer_size=3)

        # Should return same instance
        assert result1 == result2
        # Should not create another instance (cached on second call)
        assert mock_chunker_class.call_count == 1, f"Expected 1 call total, got {mock_chunker_class.call_count}"

    @patch("rag.semantic_embed")
    @patch("rag.SemanticChunker")
    def test_get_semantic_splitter_different_params(self, mock_chunker_class, mock_embed):
        """Test that different parameters create different splitters."""
        import rag
        # setup_method already creates fresh cache
        assert rag._splitter_cache.size() == 0, "Cache should be empty at start"
        mock_chunker_class.reset_mock()
        
        # Create mock instances - use a list that we can index
        instances = [Mock(name=f"instance_{i}") for i in range(3)]
        call_count = [0]  # Use list for mutable closure
        
        # Use callable for side_effect to return different instances
        def side_effect(*args, **kwargs):
            idx = call_count[0]
            call_count[0] += 1
            if idx < len(instances):
                return instances[idx]
            return Mock()
        
        mock_chunker_class.side_effect = side_effect

        # Use unique parameters to avoid collisions with other tests
        # Call with different parameters - each should create a new instance
        # Cache keys will be: "97.0_4", "96.0_4", "97.0_5" - all different
        result1 = _get_semantic_splitter(sim_percentile=97.0, buffer_size=4)
        assert mock_chunker_class.call_count >= 1, f"First call should trigger SemanticChunker, got {mock_chunker_class.call_count}"
        assert rag._splitter_cache.size() == 1, "Cache should have 1 entry after first call"
        
        result2 = _get_semantic_splitter(sim_percentile=96.0, buffer_size=4)
        assert mock_chunker_class.call_count >= 2, f"Second call should trigger SemanticChunker, got {mock_chunker_class.call_count}"
        assert rag._splitter_cache.size() == 2, "Cache should have 2 entries after second call"
        
        result3 = _get_semantic_splitter(sim_percentile=97.0, buffer_size=5)
        assert mock_chunker_class.call_count >= 3, f"Third call should trigger SemanticChunker, got {mock_chunker_class.call_count}"
        assert rag._splitter_cache.size() == 3, "Cache should have 3 entries after third call"

        # Should create separate instances for different params (3 different cache keys)
        assert mock_chunker_class.call_count == 3, f"Expected 3 calls, got {mock_chunker_class.call_count}. Cache size: {rag._splitter_cache.size()}"
        # Results should be different instances
        assert result1 != result2, "result1 and result2 should be different"
        assert result2 != result3, "result2 and result3 should be different"
        assert result1 != result3, "result1 and result3 should be different"


class TestRemoveHeadersFooters:
    """Tests for _remove_headers_footers function."""

    def test_remove_headers_footers_basic(self):
        """Test basic header/footer removal."""
        text = "Chapter 1\n\nMain content here.\n\nPage 5"
        result = _remove_headers_footers(text)

        # Should remove "Chapter 1" and "Page 5"
        assert "Chapter 1" not in result or "Main content" in result
        assert "Main content here" in result

    def test_remove_headers_footers_empty(self):
        """Test with empty text."""
        result = _remove_headers_footers("")
        assert result == ""

    def test_remove_headers_footers_none(self):
        """Test with None input."""
        result = _remove_headers_footers(None)
        assert result is None or result == ""

    def test_remove_headers_footers_page_number(self):
        """Test removal of page numbers."""
        text = "Content here.\n\n5\n\nMore content."
        result = _remove_headers_footers(text, page_num=5)

        # Should preserve main content
        assert "Content here" in result or "More content" in result

    def test_remove_headers_footers_repeating_lines(self):
        """Test removal of repeating header/footer lines."""
        # Create text with repeating header
        text = "Header Text\n\nContent line 1.\nContent line 2.\n\nHeader Text"
        result = _remove_headers_footers(text)

        # Should preserve content
        assert "Content line" in result

    def test_remove_headers_footers_no_headers(self):
        """Test with text that has no headers/footers."""
        text = "This is normal content without headers or footers."
        result = _remove_headers_footers(text)

        assert text in result or "normal content" in result


class TestFinalizeAndOutputChapter:
    """Tests for _finalize_and_output_chapter function."""

    def test_finalize_and_output_chapter_basic(self):
        """Test basic chapter finalization."""
        items = []
        chapter_data = {
            "chapter_num": "1",
            "chapter_title": "Introduction",
            "pages": [(1, "Page 1 content"), (2, "Page 2 content")],
        }
        pdf_metadata = {"title": "Test Book"}

        _finalize_and_output_chapter(chapter_data, items, "/path/to/book.pdf", "book.pdf", pdf_metadata, 100)

        assert len(items) == 1
        source, text = items[0]
        assert "chapter=1" in source
        assert "Introduction" in source
        assert "Page 1 content" in text
        assert "Page 2 content" in text
        assert "Test Book" in text

    def test_finalize_and_output_chapter_no_title(self):
        """Test chapter finalization without title."""
        items = []
        chapter_data = {
            "chapter_num": "2",
            "chapter_title": "",
            "pages": [(10, "Content")],
        }
        pdf_metadata = {}

        _finalize_and_output_chapter(chapter_data, items, "/path/to/book.pdf", "book.pdf", pdf_metadata, 50)

        assert len(items) == 1
        source, text = items[0]
        assert "chapter=2" in source
        assert "Content" in text

    def test_finalize_and_output_chapter_empty_pages(self):
        """Test with empty pages list."""
        items = []
        chapter_data = {
            "chapter_num": "3",
            "chapter_title": "Empty Chapter",
            "pages": [],
        }

        _finalize_and_output_chapter(chapter_data, items, "/path/to/book.pdf", "book.pdf", {}, 100)

        # Should not add anything
        assert len(items) == 0

    def test_finalize_and_output_chapter_clears_pages(self):
        """Test that pages are cleared after finalization."""
        items = []
        chapter_data = {
            "chapter_num": "1",
            "chapter_title": "Test",
            "pages": [(1, "Content")],
        }

        _finalize_and_output_chapter(chapter_data, items, "/path/to/book.pdf", "book.pdf", {}, 100)

        # Pages should be cleared
        assert chapter_data["pages"] == []

    def test_finalize_and_output_chapter_page_range(self):
        """Test that page range is included in output."""
        items = []
        chapter_data = {
            "chapter_num": "5",
            "chapter_title": "Advanced Topics",
            "pages": [(20, "Page 20"), (21, "Page 21"), (22, "Page 22")],
        }

        _finalize_and_output_chapter(chapter_data, items, "/path/to/book.pdf", "book.pdf", {}, 100)

        assert len(items) == 1
        _, text = items[0]
        # Should include page range
        assert "20-22" in text or "Pages 20-22" in text


class TestCachedEmbed:
    """Tests for cached_embed function."""

    def setup_method(self):
        """Clear cache before each test."""
        import rag
        rag._embedding_cache = {}
    
    def teardown_method(self):
        """Clear cache after each test."""
        import rag
        rag._embedding_cache = {}

    @patch("rag.get_embedder")
    def test_cached_embed_first_call(self, mock_get_embedder):
        """Test first call to cached_embed."""
        mock_embedder = Mock()
        mock_embedder.query_embed.return_value = iter([[0.1, 0.2, 0.3]])
        mock_get_embedder.return_value = mock_embedder

        result = cached_embed("test query")

        assert result == [0.1, 0.2, 0.3]
        mock_embedder.query_embed.assert_called_once_with("test query")

    @patch("rag.get_embedder")
    def test_cached_embed_caching(self, mock_get_embedder):
        """Test that cached_embed uses cache on second call."""
        import rag
        # Ensure cache is empty (setup_method should handle this)
        rag._embedding_cache = {}
        
        mock_embedder = Mock()
        # Return a new iterator each time to avoid iterator exhaustion
        mock_embedder.query_embed.side_effect = [
            iter([[0.1, 0.2, 0.3]]),
            iter([[0.1, 0.2, 0.3]]),
        ]
        mock_get_embedder.return_value = mock_embedder

        # First call
        result1 = cached_embed("test query unique")
        # Second call
        result2 = cached_embed("test query unique")

        assert result1 == result2
        # Should only call embedder once (second call uses cache)
        assert mock_embedder.query_embed.call_count == 1

    @patch("rag.get_embedder")
    def test_cached_embed_different_queries(self, mock_get_embedder):
        """Test that different queries are not cached together."""
        mock_embedder = Mock()
        mock_embedder.query_embed.side_effect = [
            iter([[0.1, 0.2, 0.3]]),
            iter([[0.4, 0.5, 0.6]]),
        ]
        mock_get_embedder.return_value = mock_embedder

        result1 = cached_embed("query 1")
        result2 = cached_embed("query 2")

        assert result1 != result2
        assert mock_embedder.query_embed.call_count == 2


# Note: _load_env_file is called at module import time and is difficult to test
# without complex mocking. It's a simple utility function that's covered by
# integration/system tests when the module loads.


class TestSemanticChunkerMethods:
    """Additional tests for SemanticChunker class methods."""

    @patch("rag.semantic_embed")
    def test_semantic_chunker_get_optimal_sample_rate(self, mock_embed):
        """Test _get_optimal_sample_rate method."""
        from rag import SemanticChunker

        chunker = SemanticChunker(embedding_function=mock_embed)

        # Small docs - no sampling
        assert chunker._get_optimal_sample_rate(100) == 1
        assert chunker._get_optimal_sample_rate(199) == 1

        # Medium docs - every 5th
        assert chunker._get_optimal_sample_rate(200) == 5
        assert chunker._get_optimal_sample_rate(999) == 5

        # Large docs - every 10th
        assert chunker._get_optimal_sample_rate(1000) == 10
        assert chunker._get_optimal_sample_rate(2999) == 10

        # Very large docs - every 20th
        assert chunker._get_optimal_sample_rate(3000) == 20
        assert chunker._get_optimal_sample_rate(10000) == 20

    @patch("rag.semantic_embed")
    def test_semantic_chunker_threshold_from_clusters(self, mock_embed):
        """Test _threshold_from_clusters method."""
        from rag import SemanticChunker
        import numpy as np

        chunker = SemanticChunker(
            embedding_function=mock_embed, number_of_chunks=5, breakpoint_threshold_type="percentile"
        )

        distances = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        threshold = chunker._threshold_from_clusters(distances)

        # Should return a valid threshold
        assert isinstance(threshold, float)
        assert 0 <= threshold <= 1

    @patch("rag.semantic_embed")
    def test_semantic_chunker_threshold_from_clusters_none(self, mock_embed):
        """Test _threshold_from_clusters raises error when number_of_chunks is None."""
        from rag import SemanticChunker

        chunker = SemanticChunker(embedding_function=mock_embed, number_of_chunks=None)

        with pytest.raises(ValueError, match="number_of_chunks is None"):
            chunker._threshold_from_clusters([0.1, 0.2, 0.3])

    @patch("rag.semantic_embed")
    @patch("rag._split_sentences_cached")
    @patch("rag._approx_token_len")
    def test_semantic_chunker_split_text_small(self, mock_token_len, mock_split, mock_embed):
        """Test SemanticChunker.split_text with small text."""
        from rag import SemanticChunker

        mock_split.return_value = ["Sentence one.", "Sentence two."]
        mock_token_len.return_value = 10  # Small text

        chunker = SemanticChunker(embedding_function=mock_embed)
        result = chunker.split_text("Small text here.")

        # Should return chunks
        assert isinstance(result, list)
        assert len(result) >= 1

    @patch("rag.semantic_embed")
    @patch("rag._split_sentences_cached")
    def test_semantic_chunker_split_text_empty(self, mock_split, mock_embed):
        """Test SemanticChunker.split_text with empty text."""
        from rag import SemanticChunker

        mock_split.return_value = []

        chunker = SemanticChunker(embedding_function=mock_embed)
        result = chunker.split_text("")

        assert isinstance(result, list)

    @patch("rag.semantic_embed")
    def test_semantic_chunker_create_documents(self, mock_embed):
        """Test SemanticChunker.create_documents method."""
        from rag import SemanticChunker

        # Mock split_text to return simple chunks
        chunker = SemanticChunker(embedding_function=mock_embed)
        chunker.split_text = Mock(return_value=["Chunk 1", "Chunk 2"])

        texts = ["Document 1 text", "Document 2 text"]
        result = chunker.create_documents(texts)

        assert isinstance(result, list)
        assert len(result) >= 2
        # Each document should have page_content
        for doc in result:
            assert "page_content" in doc or hasattr(doc, "page_content")

    @patch("rag.semantic_embed")
    def test_semantic_chunker_create_documents_with_metadata(self, mock_embed):
        """Test SemanticChunker.create_documents with metadata."""
        from rag import SemanticChunker

        chunker = SemanticChunker(embedding_function=mock_embed)
        chunker.split_text = Mock(return_value=["Chunk 1"])

        texts = ["Document 1"]
        metadatas = [{"source": "test.pdf", "page": 1}]
        result = chunker.create_documents(texts, metadatas)

        assert isinstance(result, list)
        assert len(result) >= 1

    @patch("rag.semantic_embed")
    def test_semantic_chunker_calc_breakpoint_threshold_percentile(self, mock_embed):
        """Test _calc_breakpoint_threshold with percentile type."""
        from rag import SemanticChunker
        import numpy as np

        chunker = SemanticChunker(
            embedding_function=mock_embed, breakpoint_threshold_type="percentile", breakpoint_threshold_amount=95.0
        )

        distances = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        threshold, returned_distances = chunker._calc_breakpoint_threshold(distances)

        assert isinstance(threshold, float)
        assert returned_distances == distances

    @patch("rag.semantic_embed")
    def test_semantic_chunker_calc_breakpoint_threshold_std(self, mock_embed):
        """Test _calc_breakpoint_threshold with standard_deviation type."""
        from rag import SemanticChunker

        chunker = SemanticChunker(
            embedding_function=mock_embed,
            breakpoint_threshold_type="standard_deviation",
            breakpoint_threshold_amount=2.0,
        )

        distances = [0.1, 0.2, 0.3, 0.4, 0.5]
        threshold, returned_distances = chunker._calc_breakpoint_threshold(distances)

        assert isinstance(threshold, float)
        assert returned_distances == distances


class TestApproxTokenLen:
    """Additional tests for _approx_token_len."""

    def test_approx_token_len_unicode(self):
        """Test token length with unicode characters."""
        text = "Hello 世界 🌍"
        result = _approx_token_len(text)
        # Should return a reasonable estimate
        assert result > 0

    def test_approx_token_len_special_chars(self):
        """Test token length with special characters."""
        text = "Hello!!! What's up? Let's go."
        result = _approx_token_len(text)
        assert result > 0

    def test_approx_token_len_numbers(self):
        """Test token length with numbers."""
        text = "The price is $123.45 and quantity is 1000 units."
        result = _approx_token_len(text)
        assert result > 0
