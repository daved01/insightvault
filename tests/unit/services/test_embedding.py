from unittest.mock import Mock, patch

import numpy as np
import pytest

from insightvault.services.embedding import EmbeddingService


class TestEmbeddingService:
    @pytest.fixture
    def mock_embeddings(self):
        """Create mock embeddings array"""
        return np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])

    @pytest.fixture
    async def embedding_service(self):
        """Create embedding service with mocked client"""
        with patch(
            "insightvault.services.embedding.SentenceTransformer"
        ) as mock_transformer:
            mock_client = Mock()
            mock_client.encode.return_value = np.array([[0.1, 0.2, 0.3]])
            mock_transformer.return_value = mock_client

            service = EmbeddingService(model_name="test-model")
            # Wait for the loading task to complete
            await service.loading_task
            return service

    @pytest.mark.asyncio
    async def test_load_model_initializes_client(self):
        """Test that _load_model initializes the client"""
        with patch(
            "insightvault.services.embedding.SentenceTransformer"
        ) as mock_transformer:
            service = EmbeddingService(model_name="test-model")
            await service.loading_task

            mock_transformer.assert_called_once_with("test-model")
            assert service.client == mock_transformer.return_value

    @pytest.mark.asyncio
    async def test_get_client_returns_loaded_client(self, embedding_service):
        """Test that get_client returns the loaded client"""
        service = await embedding_service
        client = await service.get_client()
        assert client == service.client

    @pytest.mark.asyncio
    async def test_get_client_waits_for_loading(self):
        """Test that get_client waits for client loading"""
        with patch(
            "insightvault.services.embedding.SentenceTransformer"
        ) as mock_transformer:
            mock_client = Mock()
            mock_transformer.return_value = mock_client

            service = EmbeddingService()
            client = await service.get_client()

            assert client == mock_client
            mock_transformer.assert_called_once()

    @pytest.mark.asyncio
    async def test_embed_returns_list_of_embeddings(
        self, embedding_service, mock_embeddings
    ):
        """Test that embed returns correct format"""
        service = await embedding_service
        service.client.encode.return_value = mock_embeddings
        texts = ["First text", "Second text"]
        expected_num_embeddings = 2

        result = await service.embed(texts)

        assert isinstance(result, list)
        assert len(result) == expected_num_embeddings
        assert isinstance(result[0], list)
        assert result[0] == [0.1, 0.2, 0.3]
        assert result[1] == [0.4, 0.5, 0.6]

    @pytest.mark.asyncio
    async def test_embed_calls_encode_with_correct_params(self, embedding_service):
        """Test that embed calls encode with correct parameters"""
        texts = ["Test text"]
        service = await embedding_service
        await service.embed(texts)

        service.client.encode.assert_called_once_with(
            texts, batch_size=32, show_progress_bar=False, convert_to_numpy=True
        )

    @pytest.mark.asyncio
    async def test_embed_with_empty_list(self, embedding_service):
        """Test embedding empty list of texts"""
        service = await embedding_service
        service.client.encode.return_value = np.array([])

        result = await service.embed([])

        assert result == []
        service.client.encode.assert_called_once_with(
            [], batch_size=32, show_progress_bar=False, convert_to_numpy=True
        )

    @pytest.mark.asyncio
    async def test_custom_model_name(self):
        """Test service initialization with custom model name"""
        custom_model = "custom-bert-model"
        with patch(
            "insightvault.services.embedding.SentenceTransformer"
        ) as mock_transformer:
            service = EmbeddingService(model_name=custom_model)
            await service.loading_task  # Wait for initialization to complete

            mock_transformer.assert_called_once_with(custom_model)
            assert service.model_name == custom_model
        assert service.model_name == custom_model

    @pytest.mark.asyncio
    async def test_embed_loads_client_if_none(self):
        """Test that embed loads client if not already loaded"""
        with patch(
            "insightvault.services.embedding.SentenceTransformer"
        ) as mock_transformer:
            mock_client = Mock()
            mock_client.encode.return_value = np.array([[0.1, 0.2, 0.3]])
            mock_transformer.return_value = mock_client

            service = EmbeddingService()
            service.client = None  # Reset client

            await service.embed(["test"])

            assert service.client is not None
            mock_transformer.assert_called_once()
