from unittest.mock import Mock, patch

import pytest

from insightvault.models.database import DistanceFunction
from insightvault.models.document import Document
from insightvault.services.database import ChromaDatabaseService


@pytest.fixture
def mock_collection():
    """Create a mock Chroma collection"""
    collection = Mock()
    collection.add = Mock()
    collection.query = Mock()
    collection.get = Mock()
    return collection


@pytest.fixture
def mock_client():
    """Create a mock Chroma client"""
    client = Mock()
    client.get_or_create_collection = Mock()
    client.get_collection = Mock()
    client.delete_collection = Mock()
    return client


@pytest.fixture
async def db_service(mock_client):
    """Create database service with mocked client"""
    service = ChromaDatabaseService(persist_directory="test/db")
    service.client = mock_client
    return service


@pytest.fixture
def sample_documents():
    """Create sample documents for testing"""
    return [
        Document(
            id="1",
            title="Doc 1",
            content="Content 1",
            metadata={"source": "test"},
            embedding=[0.1, 0.2, 0.3],
        ),
        Document(
            id="2",
            title="Doc 2",
            content="Content 2",
            metadata={"source": "test"},
            embedding=[0.4, 0.5, 0.6],
        ),
    ]


@pytest.mark.asyncio
@patch("insightvault.services.database.chromadb")
async def test_init_creates_client(mock_chromadb):
    """Test database initialization"""
    service = ChromaDatabaseService()
    await service.init()

    mock_chromadb.PersistentClient.assert_called_once_with(
        path="data/.db",
        settings=mock_chromadb.Settings.return_value,
    )


@pytest.mark.asyncio
async def test_add_documents(db_service, mock_collection, sample_documents):
    """Test adding documents to database"""
    db_service.client.get_or_create_collection.return_value = mock_collection

    await db_service.add_documents(sample_documents)

    mock_collection.add.assert_called_once_with(
        documents=[doc.content for doc in sample_documents],
        metadatas=[doc.metadata for doc in sample_documents],
        embeddings=[doc.embedding for doc in sample_documents],
        ids=[doc.id for doc in sample_documents],
    )


@pytest.mark.asyncio
async def test_query_returns_documents(db_service, mock_collection):
    """Test querying documents"""
    mock_collection.query.return_value = {
        "ids": [["1"]],
        "documents": [["Content"]],
        "metadatas": [[{"title": "Doc", "source": "test"}]],
        "distances": [[0.95]],
    }
    db_service.client.get_collection.return_value = mock_collection

    results = await db_service.query([0.1, 0.2, 0.3])

    assert len(results) == 1
    assert results[0].title == "Doc"
    assert results[0].content == "Content"


@pytest.mark.asyncio
async def test_get_documents(db_service, mock_collection):
    """Test retrieving all documents"""
    mock_collection.get.return_value = {
        "ids": ["1", "2"],
        "documents": ["Content 1", "Content 2"],
        "metadatas": [
            {"title": "Doc 1", "source": "test"},
            {"title": "Doc 2", "source": "test"},
        ],
    }
    db_service.client.get_collection.return_value = mock_collection

    documents = await db_service.get_documents()

    assert len(documents) == 2
    assert documents[0].title == "Doc 1"
    assert documents[1].title == "Doc 2"


@pytest.mark.asyncio
async def test_delete_all_documents(db_service):
    """Test deleting all documents"""
    await db_service.delete_all_documents()
    db_service.client.delete_collection.assert_called_once()


@pytest.mark.asyncio
async def test_query_with_filtering(db_service, mock_collection):
    """Test query with document filtering"""
    mock_collection.query.return_value = {
        "ids": [["1", "2"]],
        "documents": [["Content 1", "Content 2"]],
        "metadatas": [[{"title": "Doc 1"}, {"title": "Doc 2"}]],
        "distances": [[0.95, 0.85]],  # Second document below threshold
        "embeddings": [[None, None]],
        "data": [[None, None]],
    }
    db_service.client.get_collection.return_value = mock_collection

    results = await db_service.query([0.1, 0.2, 0.3], filter_docs=True)

    assert len(results) == 1
    assert results[0].title == "Doc 1"


def test_get_db_value_returns_correct_string():
    """Test distance function conversion"""
    service = ChromaDatabaseService()

    assert service._get_db_value(DistanceFunction.COSINE) == "cosine"
    assert service._get_db_value(DistanceFunction.L2) == "l2"


@pytest.mark.asyncio
async def test_query_handles_collection_error(db_service):
    """Test query error handling"""
    db_service.client.get_collection.side_effect = Exception("Collection not found")

    results = await db_service.query([0.1, 0.2, 0.3])

    assert results == []


@pytest.mark.asyncio
async def test_get_documents_handles_collection_error(db_service):
    """Test get_documents error handling"""
    db_service.client.get_collection.side_effect = Exception("Collection not found")

    results = await db_service.get_documents()

    assert results == []
