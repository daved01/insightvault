import pytest

from insightvault.models.document import Document


class BaseTest:
    """Base class for all unit tests"""

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
    def sample_documents(self):
        """Create sample retrieved documents"""
        return [
            Document(
                title="Doc 1",
                content="Content from first document",
                metadata={"source": "test"},
            ),
            Document(
                title="Doc 2",
                content="Content from second document",
                metadata={"source": "test"},
            ),
        ]
