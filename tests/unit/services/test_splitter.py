from unittest.mock import patch

import pytest

from insightvault.models.document import Document
from insightvault.services.splitter import SplitterService


class TestSplitterService:
    @pytest.fixture
    def sample_document(self):
        """Create a sample document for testing"""
        return Document(
            title="Test Document",
            content="This is a test document. It has multiple sentences. "
            "We will use it to test the splitter service. "
            "It should be split into chunks.",
            metadata={"source": "test"},
        )

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
    def splitter(self, mock_splitter):
        """Create a splitter service with mocked sentence splitter"""
        return SplitterService(chunk_size=50, chunk_overlap=10)

    def test_split_document_creates_chunks(self, splitter, sample_document):
        """Test that split creates multiple chunks from a document"""
        chunks = splitter.split(sample_document)

        assert len(chunks) == 3
        assert all(isinstance(chunk, Document) for chunk in chunks)

    def test_splitter_initialization(self, mock_splitter):
        """Test splitter initialization with custom parameters"""
        _ = SplitterService(chunk_size=100, chunk_overlap=20)

        mock_splitter.assert_called_once_with(chunk_size=100, chunk_overlap=20)

    def test_split_document_preserves_metadata(self, splitter, sample_document):
        """Test that split preserves and extends document metadata"""
        chunks = splitter.split(sample_document)

        for i, chunk in enumerate(chunks):
            # Original metadata is preserved
            assert chunk.metadata["source"] == sample_document.metadata["source"]
            # New metadata is added
            assert chunk.metadata["chunk_index"] == str(i)
            assert chunk.metadata["total_chunks"] == str(len(chunks))

    def test_split_document_preserves_timestamps(self, splitter, sample_document):
        """Test that split preserves document timestamps"""
        chunks = splitter.split(sample_document)

        for chunk in chunks:
            assert chunk.created_at == sample_document.created_at
            assert chunk.updated_at == sample_document.updated_at

    def test_split_document_preserves_title(self, splitter, sample_document):
        """Test that split preserves document title"""
        chunks = splitter.split(sample_document)

        for chunk in chunks:
            assert chunk.title == sample_document.title

    def test_split_empty_document(self, splitter):
        """Test splitting an empty document"""
        empty_doc = Document(
            title="Empty Doc",
            content="",
            metadata={"source": "test"},
        )

        with patch.object(splitter.text_splitter, "split_text", return_value=[""]):
            chunks = splitter.split(empty_doc)

            assert len(chunks) == 1
            assert chunks[0].content == ""

    def test_splitter_calls_split_text_with_content(self, splitter, sample_document):
        """Test that splitter calls split_text with document content"""
        splitter.split(sample_document)

        splitter.text_splitter.split_text.assert_called_once_with(
            sample_document.content
        )
