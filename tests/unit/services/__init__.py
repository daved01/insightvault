import pytest

from insightvault.models.document import Document


class BaseTest:
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
