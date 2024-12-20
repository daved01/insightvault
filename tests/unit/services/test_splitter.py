from unittest.mock import patch

import pytest

from insightvault.models.document import Document
from insightvault.services.splitter import SplitterService
from tests.unit import BaseTest


class TestSplitterService(BaseTest):
    @pytest.fixture
    def mock_splitter(self):
        """Create a mock sentence splitter"""
        with patch("insightvault.services.splitter.SentenceSplitter") as mock:
            splitter_instance = mock.return_value
            splitter_instance.split_text.return_value = [
                "First chunk of text.",
                "Second chunk of text.",
                "Third chunk of text.",
            ]
            yield mock

    @pytest.fixture
    def mock_splitter_service(self, mock_splitter):
        """Create a splitter service with mocked sentence splitter"""
        return SplitterService(chunk_size=50, chunk_overlap=10)

    def test_split_document_creates_chunks(
        self, mock_splitter_service, sample_document
    ):
        """Test that split creates multiple chunks from a document"""
        chunks = mock_splitter_service.split(sample_document)

        expected_chunks_count = 3
        assert len(chunks) == expected_chunks_count
        assert all(isinstance(chunk, Document) for chunk in chunks)

    def test_splitter_initialization(self, mock_splitter):
        """Test splitter initialization with custom parameters"""
        _ = SplitterService(chunk_size=100, chunk_overlap=20)

        mock_splitter.assert_called_once_with(chunk_size=100, chunk_overlap=20)

    def test_split_document_preserves_metadata(
        self, mock_splitter_service, sample_document
    ):
        """Test that split preserves and extends document metadata"""
        chunks = mock_splitter_service.split(sample_document)

        for i, chunk in enumerate(chunks):
            # Original metadata is preserved
            assert chunk.metadata["source"] == sample_document.metadata["source"]
            # New metadata is added
            assert chunk.metadata["chunk_index"] == str(i)
            assert chunk.metadata["total_chunks"] == str(len(chunks))

    def test_split_document_preserves_timestamps(
        self, mock_splitter_service, sample_document
    ):
        """Test that split preserves document timestamps"""
        chunks = mock_splitter_service.split(sample_document)

        for chunk in chunks:
            assert chunk.created_at == sample_document.created_at
            assert chunk.updated_at == sample_document.updated_at

    def test_split_document_preserves_title(
        self, mock_splitter_service, sample_document
    ):
        """Test that split preserves document title"""
        chunks = mock_splitter_service.split(sample_document)

        for chunk in chunks:
            assert chunk.title == sample_document.title

    def test_split_empty_document(self, mock_splitter_service):
        """Test splitting an empty document"""
        empty_doc = Document(
            title="Empty Doc",
            content="",
            metadata={"source": "test"},
        )

        with patch.object(
            mock_splitter_service.text_splitter, "split_text", return_value=[""]
        ):
            chunks = mock_splitter_service.split(empty_doc)

            assert len(chunks) == 1
            assert chunks[0].content == ""

    def test_splitter_calls_split_text_with_content(
        self, mock_splitter_service, sample_document
    ):
        """Test that splitter calls split_text with document content"""
        mock_splitter_service.split(sample_document)

        mock_splitter_service.text_splitter.split_text.assert_called_once_with(
            sample_document.content
        )
