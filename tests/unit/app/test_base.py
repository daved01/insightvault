from unittest.mock import AsyncMock, Mock, patch

import pytest

from insightvault.app.base import BaseApp
from insightvault.models.document import Document
from tests.unit import BaseTest


class BaseAppTestSetup(BaseTest):
    @pytest.fixture
    def mock_embedding_service(self):
        """Create a mock embedding service"""
        service = AsyncMock()
        service.init = AsyncMock()
        service.embed = AsyncMock(return_value=[[0.1, 0.2], [0.3, 0.4]])
        return service

    @pytest.fixture
    def mock_db_service(self):
        """Create a mock database service"""
        service = AsyncMock()
        service.add_documents = AsyncMock()
        service.delete_all_documents = AsyncMock()
        service.get_documents = AsyncMock()
        return service

    @pytest.fixture
    def mock_splitter_service(self):
        """Create a mock splitter service"""
        service = Mock()
        service.split.return_value = [
            Document(
                title="Chunk 1", content="First chunk", metadata={"source": "test"}
            ),
            Document(
                title="Chunk 2", content="Second chunk", metadata={"source": "test"}
            ),
        ]
        return service

    @pytest.fixture
    def base_app(
        self,
        mock_db_service,
        mock_splitter_service,
        mock_embedding_service,
        mock_app_config,
    ):
        """Create a base app with mocked services"""
        with (
            patch("insightvault.app.base.ChromaDatabaseService") as mock_db_class,
            patch("insightvault.app.base.SplitterService") as mock_splitter_class,
            patch("insightvault.app.base.EmbeddingService") as mock_embedding_class,
            patch("insightvault.app.base.BaseApp._get_config") as mock_get_config,
        ):
            mock_db_class.return_value = mock_db_service
            mock_splitter_class.return_value = mock_splitter_service
            mock_embedding_class.return_value = mock_embedding_service
            mock_get_config.return_value = mock_app_config

            app = BaseApp()
            return app

    @pytest.fixture
    def sample_document(self):
        """Create a sample document"""
        return Document(
            title="Test Doc", content="Test content", metadata={"source": "test"}
        )


class TestBaseApp(BaseAppTestSetup):
    @pytest.mark.asyncio
    async def test_init_initializes_services(self, base_app):
        """Test that init initializes all required services"""
        await base_app.init()

        base_app.embedder_service.init.assert_called_once()
        assert base_app.name == "insightvault.app.base"

    @pytest.mark.asyncio
    async def test_add_documents_processes_correctly(self, base_app, sample_document):
        """Test that add_documents processes documents correctly"""
        await base_app.init()
        await base_app.async_add_documents([sample_document])

        # Verify splitter was called
        base_app.splitter_service.split.assert_called_once_with(sample_document)

        # Verify embedder was called with chunk contents
        base_app.embedder_service.embed.assert_called_once_with(
            ["First chunk", "Second chunk"]
        )

        # Verify documents were added to db with embeddings
        processed_docs = base_app.db_service.add_documents.call_args[0][0]
        expected_num_processed_docs = 2
        assert len(processed_docs) == expected_num_processed_docs
        assert processed_docs[0].embedding == [0.1, 0.2]
        assert processed_docs[1].embedding == [0.3, 0.4]

    @pytest.mark.asyncio
    async def test_add_documents_without_embedder_raises_error(
        self, base_app, sample_document
    ):
        """Test add_documents fails when embedder is not initialized"""
        base_app.embedder_service = None

        with pytest.raises(RuntimeError) as exc:
            await base_app.async_add_documents([sample_document])

        assert "Embedding service is not loaded" in str(exc.value)

    @pytest.mark.asyncio
    async def test_delete_all_documents(self, base_app):
        """Test delete_all_documents calls database correctly"""
        await base_app.async_delete_all_documents()
        base_app.db_service.delete_all_documents.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_documents(self, base_app):
        """Test list_documents returns database results"""
        expected_docs = [
            Document(title="Doc 1", content="Content 1"),
            Document(title="Doc 2", content="Content 2"),
        ]
        base_app.db_service.get_documents.return_value = expected_docs

        result = await base_app.async_list_documents()

        base_app.db_service.get_documents.assert_called_once()
        assert result == expected_docs

    def test_sync_methods_call_async_versions(self, base_app):
        """Test that sync methods properly call their async counterparts"""
        with patch("asyncio.run") as mock_run:
            # Test add_documents
            base_app.add_documents([Document(title="Test", content="Content")])
            assert mock_run.called

            # Test delete_all_documents
            base_app.delete_all_documents()
            assert mock_run.called

            # Test list_documents
            base_app.list_documents()
            assert mock_run.called

    @pytest.mark.asyncio
    async def test_add_documents_preserves_metadata(self, base_app, sample_document):
        """Test that document metadata is preserved through processing"""
        await base_app.init()
        await base_app.async_add_documents([sample_document])

        processed_docs = base_app.db_service.add_documents.call_args[0][0]
        for doc in processed_docs:
            assert doc.metadata["source"] == "test"

    @pytest.mark.asyncio
    async def test_add_documents_with_empty_list(self, base_app):
        """Test adding empty document list"""
        await base_app.init()
        await base_app.async_add_documents([])

        base_app.db_service.add_documents.assert_called_once_with([])

    def test_get_config(self, base_app):
        """Test getting config file"""
        config = base_app._get_config(path="./tests/mocks/mock_config.yaml")

        expected_num_results = 12
        expected_threshold = 0.82
        expected_chunk_size = 12
        expected_chunk_overlap = 6
        assert config.database.path == "mock-path"
        assert config.database.max_num_results == expected_num_results
        assert config.database.result_threshold == expected_threshold
        assert config.splitter.chunk_size == expected_chunk_size
        assert config.splitter.chunk_overlap == expected_chunk_overlap
        assert config.llm.model == "some-model"
        assert config.embedding.model == "another-model"

    def test_get_config_should_use_defaults(self, base_app):
        """Test getting config file with incomplete config file"""
        config = base_app._get_config(path="./tests/mocks/mock_config_incomplete.yaml")

        expected_num_results = 5  # Default
        expected_threshold = 0.9  # Default
        expected_chunk_size = 12
        expected_chunk_overlap = 256  # Default
        assert config.database.path == "./data/db"
        assert config.database.max_num_results == expected_num_results
        assert config.database.result_threshold == expected_threshold
        assert config.splitter.chunk_size == expected_chunk_size
        assert config.splitter.chunk_overlap == expected_chunk_overlap
        assert config.llm.model == "some-model"
        assert config.embedding.model == "all-MiniLM-L6-v2"
