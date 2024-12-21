from unittest.mock import AsyncMock, Mock, patch

import pytest

from insightvault.app.base import BaseApp
from insightvault.models.document import Document


class BaseAppFixtures:
    @pytest.fixture(autouse=True)
    def mock_dependencies(self):
        """Mock all external dependencies"""
        with patch(
            "insightvault.app.base.EmbeddingService", autospec=True
        ) as mock_embedding_service:
            # Configure the mock embedding service
            instance = mock_embedding_service.return_value
            instance.embed = AsyncMock(return_value=[[0.1, 0.2], [0.3, 0.4]])
            instance.get_client = AsyncMock()
            yield mock_embedding_service

    @pytest.fixture
    def mock_embedding_service(self, mock_dependencies):
        """Create a mock embedding service"""
        return mock_dependencies.return_value

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
    def base_app(self, mock_db_service, mock_splitter_service):
        """Create a base app with mocked services"""
        with (
            patch("insightvault.app.base.ChromaDatabaseService") as mock_db_class,
            patch("insightvault.app.base.SplitterService") as mock_splitter_class,
        ):
            mock_db_class.return_value = mock_db_service
            mock_splitter_class.return_value = mock_splitter_service

            app = BaseApp()
            return app

    @pytest.fixture
    def sample_document(self):
        """Create a sample document"""
        return Document(
            title="Test Doc", content="Test content", metadata={"source": "test"}
        )


class TestBaseApp(BaseAppFixtures):
    @pytest.mark.asyncio
    async def test_add_documents_processes_correctly(
        self,
        base_app,
        sample_document,
    ):
        """Test that add_documents processes documents correctly"""
        await base_app.init_base()
        await base_app.async_add_documents([sample_document])

        # Verify splitter was called
        base_app.splitter.split.assert_called_once_with(sample_document)

        # Verify embedder was called with chunk contents
        base_app.embedder.embed.assert_called_once_with(["First chunk", "Second chunk"])

        # Verify documents were added to db with embeddings
        processed_docs = base_app.db.add_documents.call_args[0][0]
        expected_docs_count = 2
        assert len(processed_docs) == expected_docs_count
        assert processed_docs[0].embedding == [0.1, 0.2]
        assert processed_docs[1].embedding == [0.3, 0.4]

    @pytest.mark.asyncio
    async def test_delete_all_documents(self, base_app):
        """Test delete_all_documents calls database correctly"""
        await base_app.async_delete_all_documents()
        base_app.db.delete_all_documents.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_documents(self, base_app):
        """Test list_documents returns database results"""
        expected_docs = [
            Document(title="Doc 1", content="Content 1"),
            Document(title="Doc 2", content="Content 2"),
        ]
        base_app.db.get_documents.return_value = expected_docs

        result = await base_app.async_list_documents()

        base_app.db.get_documents.assert_called_once()
        assert result == expected_docs

    def test_sync_methods_call_async_versions(self, base_app):
        """Test that sync methods properly call their async counterparts"""
        with patch("asyncio.get_event_loop") as mock_loop:
            mock_loop.return_value.run_until_complete = Mock()

            # Test add_documents
            base_app.add_documents([Document(title="Test", content="Content")])
            mock_loop.return_value.run_until_complete.assert_called()

            # Test delete_all_documents
            base_app.delete_all_documents()
            mock_loop.return_value.run_until_complete.assert_called()

            # Test list_documents
            base_app.list_documents()
            mock_loop.return_value.run_until_complete.assert_called()

    @pytest.mark.asyncio
    async def test_add_documents_preserves_metadata(self, base_app, sample_document):
        """Test that document metadata is preserved through processing"""
        await base_app.init_base()
        await base_app.async_add_documents([sample_document])
        processed_docs = base_app.db.add_documents.call_args[0][0]
        for doc in processed_docs:
            assert doc.metadata["source"] == "test"
