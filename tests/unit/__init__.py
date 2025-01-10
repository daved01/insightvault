import pytest

from insightvault.models.config import (
    AppConfig,
    DatabaseConfig,
    EmbeddingConfig,
    LlmConfig,
    SplitterConfig,
)
from insightvault.models.document import Document


class BaseTest:
    """Base class for all unit tests"""

    @pytest.fixture
    def mock_llm_config(self):
        return LlmConfig(model="llama3")

    @pytest.fixture
    def mock_embedding_config(self):
        return EmbeddingConfig(model="all-MiniLM-L6-v2")

    @pytest.fixture
    def mock_splitter_config(self):
        return SplitterConfig(chunk_size=1024, chunk_overlap=256)

    @pytest.fixture
    def mock_database_config(self):
        return DatabaseConfig(
            path="./data/.db", result_threshold=0.9, max_num_results=5
        )

    @pytest.fixture
    def mock_app_config(
        self,
        mock_database_config,
        mock_splitter_config,
        mock_llm_config,
        mock_embedding_config,
    ):
        """Creates a mock config"""
        return AppConfig(
            database=mock_database_config,
            splitter=mock_splitter_config,
            llm=mock_llm_config,
            embedding=mock_embedding_config,
        )

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
                id="1",
                title="Doc 1",
                content="Content from first document",
                metadata={"source": "test"},
                embedding=[0.1, 0.2, 0.3],
            ),
            Document(
                id="2",
                title="Doc 2",
                content="Content from second document",
                metadata={"source": "test"},
                embedding=[0.4, 0.5, 0.6],
            ),
        ]
