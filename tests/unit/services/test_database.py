from unittest.mock import Mock, patch

import pytest

from insightvault.models.database import DistanceFunction
from insightvault.services.database import ChromaDatabaseService
from tests.unit import BaseTest


class TestChromaDatabaseService(BaseTest):
    @pytest.fixture
    def mock_collection(self):
        """Create a mock Chroma collection"""
        collection = Mock()
        collection.add = Mock()
        collection.query = Mock()
        collection.get = Mock()
        return collection

    @pytest.fixture
    def mock_client(self):
        """Create a mock Chroma client"""
        client = Mock()
        client.get_or_create_collection = Mock()
        client.get_collection = Mock()
        client.delete_collection = Mock()
        return client

    @pytest.fixture
    async def db_service(self, mock_client):
        """Create database service with mocked client"""
        with patch(
            "insightvault.services.database.chromadb.PersistentClient"
        ) as mock_chroma:
            mock_chroma.return_value = mock_client
            service = ChromaDatabaseService(persist_directory="test/db")
            return service

    @pytest.mark.asyncio
    @patch("insightvault.services.database.chromadb")
    @patch("insightvault.services.database.get_logger")
    async def test_init_creates_client(self, mock_get_logger, mock_chromadb):
        """Test database initialization"""
        # Create and initialize service
        service = ChromaDatabaseService(persist_directory="data/.db")

        # Check PersistentClient was called
        assert len(mock_chromadb.mock_calls) == 1
        call_args = mock_chromadb.PersistentClient.call_args

        # Verify the arguments
        assert call_args.kwargs["path"] == "data/.db"
        assert call_args.kwargs["settings"].anonymized_telemetry is False
        assert call_args.kwargs["settings"].allow_reset is True

        # Verify the client was set
        assert service.client == mock_chromadb.PersistentClient.return_value

    @pytest.mark.asyncio
    async def test_add_documents(self, db_service, mock_collection, sample_documents):
        """Test adding documents to database"""
        service = await db_service
        service.client.get_or_create_collection.return_value = mock_collection

        await service.add_documents(sample_documents)

        mock_collection.add.assert_called_once_with(
            documents=[doc.content for doc in sample_documents],
            metadatas=[doc.metadata for doc in sample_documents],
            embeddings=[doc.embedding for doc in sample_documents],
            ids=[doc.id for doc in sample_documents],
        )

    @pytest.mark.asyncio
    async def test_query_returns_documents(self, db_service, mock_collection):
        """Test querying documents"""
        mock_collection.query.return_value = {
            "ids": [["1"]],
            "documents": [["Content"]],
            "metadatas": [[{"title": "Doc", "source": "test"}]],
            "distances": [[0.95]],
            "embeddings": [[[0.1, 0.2, 0.3]]],
            "data": [
                [
                    {
                        "id": "1",
                        "content": "Content",
                        "metadata": {"title": "Doc", "source": "test"},
                    }
                ]
            ],
        }
        service = await db_service
        service.client.get_collection.return_value = mock_collection

        results = await service.query([0.1, 0.2, 0.3])

        assert len(results) == 1
        assert results[0].title == "Doc"
        assert results[0].content == "Content"

    @pytest.mark.asyncio
    async def test_get_documents(self, db_service, mock_collection):
        """Test retrieving all documents"""
        mock_collection.get.return_value = {
            "ids": ["1", "2"],
            "documents": ["Content 1", "Content 2"],
            "metadatas": [
                {"title": "Doc 1", "source": "test"},
                {"title": "Doc 2", "source": "test"},
            ],
        }
        service = await db_service
        service.client.get_collection.return_value = mock_collection

        documents = await service.get_documents()

        expected_docs_count = 2
        assert len(documents) == expected_docs_count
        assert documents[0].title == "Doc 1"
        assert documents[1].title == "Doc 2"

    @pytest.mark.asyncio
    async def test_delete_all_documents(self, db_service):
        """Test deleting all documents"""
        service = await db_service
        await service.delete_all_documents()
        service.client.delete_collection.assert_called_once()

    @pytest.mark.asyncio
    async def test_query_with_filtering(self, db_service, mock_collection):
        """Test query with document filtering"""
        mock_collection.query.return_value = {
            "ids": [["1", "2"]],
            "documents": [["Content 1", "Content 2"]],
            "metadatas": [[{"title": "Doc 1"}, {"title": "Doc 2"}]],
            "distances": [[0.95, 0.85]],
            "embeddings": [[None, None]],
            "data": [[None, None]],
        }
        service = await db_service
        service.client.get_collection.return_value = mock_collection

        results = await service.query([0.1, 0.2, 0.3], filter_docs=True)

        assert len(results) == 1
        assert results[0].title == "Doc 1"

    def test_get_db_value_returns_correct_string(self):
        """Test distance function conversion"""
        service = ChromaDatabaseService()

        assert service._get_db_value(DistanceFunction.COSINE) == "cosine"
        assert service._get_db_value(DistanceFunction.L2) == "l2"

    @pytest.mark.asyncio
    async def test_query_handles_collection_error(self, db_service):
        """Test query error handling"""
        service = await db_service
        service.client.get_collection.side_effect = Exception("Collection not found")

        results = await service.query([0.1, 0.2, 0.3])

        assert results == []

    @pytest.mark.asyncio
    async def test_get_documents_handles_collection_error(self, db_service):
        """Test get_documents error handling"""
        service = await db_service
        service.client.get_collection.side_effect = Exception("Collection not found")

        results = await service.get_documents()

        assert results == []
