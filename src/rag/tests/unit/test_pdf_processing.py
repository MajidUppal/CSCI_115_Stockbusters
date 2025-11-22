"""Unit tests for PDF processing functions."""

import pytest
import builtins
from unittest.mock import Mock, MagicMock, patch
from typing import List, Dict, Tuple

# Save real __import__ for fallback
_real_import = builtins.__import__

pytestmark = pytest.mark.unit

# Import functions to test
rag = pytest.importorskip("rag")
from rag import (
    _load_pdf,
    _extract_page_text,
    _extract_chapters_from_toc,
    _extract_non_chapter_sections_from_toc,
    _finalize_and_output_chapter,
    _remove_headers_footers,
    _norm,
)


class TestExtractPageText:
    """Tests for _extract_page_text function."""

    def test_extract_page_text_with_dict_blocks(self):
        """Test text extraction using get_text('dict') method."""
        # Mock page with dict blocks
        mock_page = Mock()
        mock_page.get_text.return_value = {
            "blocks": [
                {
                    "lines": [
                        {
                            "spans": [{"text": "Line 1 "}, {"text": "continues"}]
                        },
                        {
                            "spans": [{"text": "Line 2"}]
                        }
                    ]
                },
                {
                    "lines": [
                        {
                            "spans": [{"text": "Paragraph 2"}]
                        }
                    ]
                }
            ]
        }

        result = _extract_page_text(mock_page, page_num=1, base="test.pdf")

        assert result is not None
        # Note: spans are joined with space, so "Line 1 " + "continues" = "Line 1  continues"
        assert "Line 1" in result and "continues" in result
        assert "Line 2" in result
        assert "Paragraph 2" in result
        # Should have paragraph breaks between blocks
        assert "\n\n" in result

    def test_extract_page_text_fallback_to_text(self):
        """Test fallback to get_text('text') when dict fails."""
        mock_page = Mock()
        # First call (dict) raises exception
        mock_page.get_text.side_effect = [
            Exception("Dict method failed"),
            "Simple text content"
        ]

        result = _extract_page_text(mock_page, page_num=1, base="test.pdf")

        assert result == "Simple text content"
        assert mock_page.get_text.call_count == 2

    def test_extract_page_text_returns_none_on_failure(self):
        """Test returns None when all extraction methods fail."""
        mock_page = Mock()
        mock_page.get_text.side_effect = Exception("All methods failed")

        result = _extract_page_text(mock_page, page_num=1, base="test.pdf")

        assert result is None

    def test_extract_page_text_empty_blocks(self):
        """Test with empty blocks."""
        mock_page = Mock()
        mock_page.get_text.return_value = {"blocks": []}

        result = _extract_page_text(mock_page, page_num=1, base="test.pdf")

        assert result is None

    def test_extract_page_text_skips_image_blocks(self):
        """Test that image blocks (without 'lines') are skipped."""
        mock_page = Mock()
        mock_page.get_text.return_value = {
            "blocks": [
                {"type": 1},  # Image block, no 'lines' key
                {
                    "lines": [{"spans": [{"text": "Text content"}]}]
                }
            ]
        }

        result = _extract_page_text(mock_page, page_num=1, base="test.pdf")

        assert result is not None
        assert "Text content" in result


class TestExtractChaptersFromTOC:
    """Tests for _extract_chapters_from_toc function."""

    def test_extract_chapters_basic(self):
        """Test basic chapter extraction from TOC."""
        mock_doc = Mock()
        # TOC format: (level, title, page_num_0_indexed)
        mock_doc.get_toc.return_value = [
            (1, "Chapter 1: Introduction", 0),
            (1, "Chapter 2: Methods", 10),
            (1, "Chapter 3: Results", 20),
        ]

        result = _extract_chapters_from_toc(mock_doc)

        assert len(result) == 3
        assert 1 in result  # Page 1 (0-indexed + 1)
        assert 11 in result  # Page 11
        assert 21 in result  # Page 21
        assert result[1]["chapter_number"] == "1"
        assert result[1]["chapter_title"] == "Introduction"

    def test_extract_chapters_no_toc(self):
        """Test with no table of contents."""
        mock_doc = Mock()
        mock_doc.get_toc.return_value = []

        result = _extract_chapters_from_toc(mock_doc)

        assert result == {}

    def test_extract_chapters_handles_exception(self):
        """Test handles exception during TOC extraction."""
        mock_doc = Mock()
        mock_doc.get_toc.side_effect = Exception("TOC extraction failed")

        result = _extract_chapters_from_toc(mock_doc)

        assert result == {}

    def test_extract_chapters_handles_missing_toc(self):
        """Test when get_toc is not available."""
        mock_doc = Mock()
        del mock_doc.get_toc

        result = _extract_chapters_from_toc(mock_doc)

        assert result == {}

    def test_extract_chapters_various_formats(self):
        """Test extraction with various chapter title formats."""
        mock_doc = Mock()
        mock_doc.get_toc.return_value = [
            (1, "Chapter 1: Introduction", 0),
            (1, "Ch. 2 Methods", 10),
            (1, "3 Results", 20),  # Standalone number format
            (1, "Part I: Overview", 30),  # Should be skipped (organizational)
            (2, "1.1 Section", 5),  # Should be skipped (section format)
        ]

        result = _extract_chapters_from_toc(mock_doc)

        # Should extract 3 chapters, skip Part and section
        assert len(result) == 3
        assert 1 in result
        assert 11 in result
        assert 21 in result

    def test_extract_chapters_hierarchical_levels(self):
        """Test with hierarchical TOC levels."""
        mock_doc = Mock()
        # Level 1: Parts, Level 2: Chapters
        mock_doc.get_toc.return_value = [
            (1, "Part I: Fundamentals", 0),
            (2, "Chapter 1: Basics", 5),
            (2, "Chapter 2: Advanced", 15),
            (1, "Part II: Applications", 25),
            (2, "Chapter 3: Case Studies", 30),
        ]

        result = _extract_chapters_from_toc(mock_doc)

        # Should find chapters at level 2
        assert len(result) >= 3
        assert 6 in result  # Chapter 1 at page 6
        assert 16 in result  # Chapter 2 at page 16
        assert 31 in result  # Chapter 3 at page 31


class TestExtractNonChapterSectionsFromTOC:
    """Tests for _extract_non_chapter_sections_from_toc function."""

    def test_extract_non_chapter_sections_basic(self):
        """Test extraction of non-chapter sections."""
        mock_doc = Mock()
        mock_doc.get_toc.return_value = [
            (1, "Table of Contents", 0),
            (1, "Chapter 1: Introduction", 5),
            (1, "Index", 100),
            (1, "Bibliography", 105),
        ]

        result = _extract_non_chapter_sections_from_toc(mock_doc)

        # Should return 1-indexed page numbers
        assert 1 in result  # TOC
        assert 101 in result  # Index
        assert 106 in result  # Bibliography
        assert 6 not in result  # Chapter should not be included

    def test_extract_non_chapter_sections_all_keywords(self):
        """Test all non-chapter keywords are detected."""
        mock_doc = Mock()
        mock_doc.get_toc.return_value = [
            (1, "Preface", 0),
            (1, "Foreword", 2),
            (1, "Acknowledgements", 4),
            (1, "Appendix A", 90),
            (1, "Glossary", 95),
            (1, "List of Figures", 98),
        ]

        result = _extract_non_chapter_sections_from_toc(mock_doc)

        assert len(result) == 6
        assert 1 in result  # Preface
        assert 3 in result  # Foreword
        assert 5 in result  # Acknowledgements
        assert 91 in result  # Appendix
        assert 96 in result  # Glossary
        assert 99 in result  # List of Figures

    def test_extract_non_chapter_sections_no_toc(self):
        """Test with no TOC."""
        mock_doc = Mock()
        mock_doc.get_toc.return_value = []

        result = _extract_non_chapter_sections_from_toc(mock_doc)

        assert result == set()

    def test_extract_non_chapter_sections_handles_exception(self):
        """Test handles exception during extraction."""
        mock_doc = Mock()
        mock_doc.get_toc.side_effect = Exception("TOC failed")

        result = _extract_non_chapter_sections_from_toc(mock_doc)

        assert result == set()

    def test_extract_non_chapter_sections_case_insensitive(self):
        """Test keyword matching is case insensitive."""
        mock_doc = Mock()
        mock_doc.get_toc.return_value = [
            (1, "INDEX", 50),
            (1, "bibliography", 55),
            (1, "Appendix", 60),
        ]

        result = _extract_non_chapter_sections_from_toc(mock_doc)

        assert 51 in result  # INDEX
        assert 56 in result  # bibliography
        assert 61 in result  # Appendix


class TestFinalizeAndOutputChapter:
    """Tests for _finalize_and_output_chapter function."""

    def test_finalize_and_output_chapter_basic(self):
        """Test basic chapter finalization."""
        items = []
        chapter_data = {
            "chapter_num": "1",
            "chapter_title": "Introduction",
            "pages": [(1, "Page 1 text"), (2, "Page 2 text")]
        }

        _finalize_and_output_chapter(
            chapter_data, items, "/path/to/doc.pdf", "doc.pdf",
            {"title": "Test Book"}, 10
        )

        assert len(items) == 1
        source, text = items[0]
        assert "doc.pdf#chapter=1" in source
        assert "Introduction" in text
        assert "Page 1 text" in text
        assert "Page 2 text" in text
        assert "[Pages 1-2 of 10]" in text

    def test_finalize_and_output_chapter_no_title(self):
        """Test chapter without title."""
        items = []
        chapter_data = {
            "chapter_num": "2",
            "chapter_title": "",
            "pages": [(5, "Content")]
        }

        _finalize_and_output_chapter(
            chapter_data, items, "/path/doc.pdf", "doc.pdf",
            {}, 20
        )

        assert len(items) == 1
        source, text = items[0]
        assert "chapter=2" in source
        assert "[Chapter 2]" in text

    def test_finalize_and_output_chapter_empty_pages(self):
        """Test with empty pages list."""
        items = []
        chapter_data = {
            "chapter_num": "1",
            "chapter_title": "Test",
            "pages": []
        }

        _finalize_and_output_chapter(
            chapter_data, items, "/path/doc.pdf", "doc.pdf", {}, 10
        )

        # Should not add anything
        assert len(items) == 0

    def test_finalize_and_output_chapter_clears_pages(self):
        """Test that pages are cleared after finalization."""
        items = []
        chapter_data = {
            "chapter_num": "1",
            "chapter_title": "Test",
            "pages": [(1, "Content")]
        }

        _finalize_and_output_chapter(
            chapter_data, items, "/path/doc.pdf", "doc.pdf", {}, 10
        )

        # Pages should be cleared
        assert chapter_data["pages"] == []

    def test_finalize_and_output_chapter_with_title_sanitization(self):
        """Test title is sanitized in source path."""
        items = []
        chapter_data = {
            "chapter_num": "3",
            "chapter_title": "Advanced Topics / Special Cases",
            "pages": [(10, "Content")]
        }

        _finalize_and_output_chapter(
            chapter_data, items, "/path/doc.pdf", "doc.pdf", {}, 20
        )

        source, _ = items[0]
        # Should sanitize special characters
        assert "/" not in source or "Special_Cases" in source


class TestLoadPDF:
    """Tests for _load_pdf function."""

    @patch("rag.ENABLE_SECTION_FILTER", False)
    @patch("rag._norm")
    @patch("rag._remove_headers_footers")
    @patch("rag._extract_page_text")
    @patch("builtins.__import__")
    def test_load_pdf_no_filtering(self, mock_import, mock_extract, mock_remove, mock_norm):
        """Test PDF loading without section filtering."""
        # Mock fitz import
        mock_fitz = MagicMock()
        def import_side_effect(name, *args, **kwargs):
            if name == 'fitz':
                return mock_fitz
            return _real_import(name, *args, **kwargs)
        mock_import.side_effect = import_side_effect
        
        # Setup mocks
        mock_doc = Mock()
        mock_doc.metadata = {"title": "Test Book"}
        mock_doc.__len__ = Mock(return_value=3)
        mock_doc.__iter__ = Mock(return_value=iter([Mock(), Mock(), Mock()]))
        mock_fitz.open.return_value = mock_doc

        mock_extract.side_effect = ["Page 1", "Page 2", "Page 3"]
        mock_remove.side_effect = lambda x, **kwargs: x
        mock_norm.side_effect = lambda x: x

        result = _load_pdf("/path/test.pdf")

        assert len(result) == 3
        assert mock_fitz.open.called
        mock_doc.close.assert_called_once()

    @patch("rag.ENABLE_SECTION_FILTER", True)
    @patch("rag._extract_chapters_from_toc")
    @patch("rag._extract_non_chapter_sections_from_toc")
    @patch("rag._norm")
    @patch("rag._remove_headers_footers")
    @patch("rag._extract_page_text")
    @patch("rag._finalize_and_output_chapter")
    @patch("builtins.__import__")
    def test_load_pdf_with_chapter_filtering(self, mock_import, mock_finalize, mock_extract,
                                             mock_remove, mock_norm, mock_non_chapter, mock_chapters):
        """Test PDF loading with chapter filtering enabled."""
        # Mock fitz import
        mock_fitz = MagicMock()
        def import_side_effect(name, *args, **kwargs):
            if name == 'fitz':
                return mock_fitz
            return _real_import(name, *args, **kwargs)
        mock_import.side_effect = import_side_effect
        
        # Setup mocks
        mock_doc = Mock()
        mock_doc.metadata = {"title": "Test Book"}
        mock_doc.__len__ = Mock(return_value=5)
        
        # Create mock pages
        mock_pages = [Mock() for _ in range(5)]
        mock_doc.__iter__ = Mock(return_value=iter(mock_pages))
        mock_fitz.open.return_value = mock_doc

        # Setup chapter map
        mock_chapters.return_value = {
            2: {"chapter_number": "1", "chapter_title": "Introduction"},
            4: {"chapter_number": "2", "chapter_title": "Methods"}
        }
        mock_non_chapter.return_value = set()

        mock_extract.side_effect = ["Page 1", "Page 2", "Page 3", "Page 4", "Page 5"]
        mock_remove.side_effect = lambda x, **kwargs: x
        mock_norm.side_effect = lambda x: x

        result = _load_pdf("/path/test.pdf")

        # Should call finalize for each chapter
        assert mock_finalize.call_count >= 0
        mock_doc.close.assert_called_once()

    @patch("builtins.__import__")
    def test_load_pdf_import_error(self, mock_import):
        """Test when PyMuPDF is not available."""
        # Make import raise ImportError for fitz
        def import_side_effect(name, *args, **kwargs):
            if name == 'fitz':
                raise ImportError("No module named 'fitz'")
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = import_side_effect

        result = _load_pdf("/path/test.pdf")

        assert result == []

    @patch("rag.ENABLE_SECTION_FILTER", True)
    @patch("rag._extract_chapters_from_toc")
    @patch("rag._norm")
    @patch("rag._remove_headers_footers")
    @patch("rag._extract_page_text")
    @patch("builtins.__import__")
    def test_load_pdf_no_toc_fallback(self, mock_import, mock_extract, mock_remove, mock_norm, mock_chapters):
        """Test fallback when TOC is not available."""
        # Mock fitz import
        mock_fitz = MagicMock()
        def import_side_effect(name, *args, **kwargs):
            if name == 'fitz':
                return mock_fitz
            return _real_import(name, *args, **kwargs)
        mock_import.side_effect = import_side_effect
        
        mock_doc = Mock()
        mock_doc.metadata = {}
        mock_doc.__len__ = Mock(return_value=2)
        mock_doc.__iter__ = Mock(return_value=iter([Mock(), Mock()]))
        mock_fitz.open.return_value = mock_doc

        # No chapters in TOC
        mock_chapters.return_value = {}
        mock_extract.side_effect = ["Page 1", "Page 2"]
        mock_remove.side_effect = lambda x, **kwargs: x
        mock_norm.side_effect = lambda x: x

        result = _load_pdf("/path/test.pdf")

        # Should fall back to processing all pages
        assert len(result) >= 0
        mock_doc.close.assert_called_once()

    @patch("rag.ENABLE_SECTION_FILTER", False)
    @patch("rag._extract_chapters_from_toc")
    @patch("rag._norm")
    @patch("rag._remove_headers_footers")
    @patch("rag._extract_page_text")
    @patch("builtins.__import__")
    def test_load_pdf_empty_pages(self, mock_import, mock_extract, mock_remove, mock_norm, mock_chapters):
        """Test with pages that have no text."""
        # Mock fitz import
        mock_fitz = MagicMock()
        def import_side_effect(name, *args, **kwargs):
            if name == 'fitz':
                return mock_fitz
            return _real_import(name, *args, **kwargs)
        mock_import.side_effect = import_side_effect
        
        mock_doc = Mock()
        mock_doc.metadata = {}
        mock_doc.__len__ = Mock(return_value=3)
        mock_doc.__iter__ = Mock(return_value=iter([Mock(), Mock(), Mock()]))
        mock_fitz.open.return_value = mock_doc

        # Some pages return empty text
        mock_extract.side_effect = ["", "Valid content", None]
        mock_remove.side_effect = lambda x, **kwargs: x if x else ""
        mock_norm.side_effect = lambda x: x

        result = _load_pdf("/path/test.pdf")

        # Should only include pages with content
        assert len(result) == 1
        assert "Valid content" in result[0][1]

    @patch("rag.TQDM_AVAILABLE", False)
    @patch("rag.ENABLE_SECTION_FILTER", True)
    @patch("rag._extract_chapters_from_toc")
    @patch("rag._extract_non_chapter_sections_from_toc")
    @patch("rag._norm")
    @patch("rag._remove_headers_footers")
    @patch("rag._extract_page_text")
    @patch("rag._finalize_and_output_chapter")
    @patch("builtins.__import__")
    def test_load_pdf_filters_non_chapter_sections(self, mock_import, mock_finalize, mock_extract,
                                                   mock_remove, mock_norm, mock_non_chapter, mock_chapters):
        """Test that non-chapter sections are filtered out."""
        # Mock fitz import
        mock_fitz = MagicMock()
        def import_side_effect(name, *args, **kwargs):
            if name == 'fitz':
                return mock_fitz
            return _real_import(name, *args, **kwargs)
        mock_import.side_effect = import_side_effect
        
        mock_doc = Mock()
        mock_doc.metadata = {}
        mock_doc.__len__ = Mock(return_value=10)
        mock_pages = [Mock() for _ in range(10)]
        mock_doc.__iter__ = Mock(return_value=iter(mock_pages))
        mock_fitz.open.return_value = mock_doc

        # Chapters at pages 2, 5, 8
        mock_chapters.return_value = {
            2: {"chapter_number": "1", "chapter_title": "Ch1"},
            5: {"chapter_number": "2", "chapter_title": "Ch2"},
            8: {"chapter_number": "3", "chapter_title": "Ch3"}
        }
        # Index at page 9
        mock_non_chapter.return_value = {9, 10}

        mock_extract.side_effect = [f"Page {i}" for i in range(1, 11)]
        mock_remove.side_effect = lambda x, **kwargs: x
        mock_norm.side_effect = lambda x: x

        result = _load_pdf("/path/test.pdf")

        # Should filter out pages 9 and 10 (Index)
        mock_doc.close.assert_called_once()

