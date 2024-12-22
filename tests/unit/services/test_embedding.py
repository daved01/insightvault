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
            # Configure the mock transformer
            mock_transformer.return_value = Mock()
            mock_transformer.return_value.encode = Mock(
                return_value=np.array([[0.1, 0.2, 0.3]])
            )

            service = EmbeddingService(model_name="test-model")
            service.client = mock_transformer.return_value
            return service

    @pytest.mark.asyncio
    async def test_init_loads_model(self):
        with patch(
            "insightvault.services.embedding.SentenceTransformer"
        ) as mock_transformer:
            service = EmbeddingService(model_name="test-model")
            await service.init()

            mock_transformer.assert_called_once_with("test-model")
            assert service.client == mock_transformer.return_value

    @pytest.mark.asyncio
    async def test_embed_returns_list_of_embeddings(
        self, embedding_service, mock_embeddings
    ):
        service = await embedding_service
        service.client.encode.return_value = mock_embeddings
        texts = ["First text", "Second text"]

        result = await service.embed(texts)

        assert isinstance(result, list)
        assert len(result) == len(texts)
        assert isinstance(result[0], list)
        assert result[0] == [0.1, 0.2, 0.3]
        assert result[1] == [0.4, 0.5, 0.6]

    @pytest.mark.asyncio
    async def test_embed_calls_encode_with_correct_params(self, embedding_service):
        service = await embedding_service
        texts = ["Test text"]
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

    def test_custom_model_name(self):
        """Test service initialization with custom model name"""
        custom_model = "custom-bert-model"
        service = EmbeddingService(model_name=custom_model)
        assert service.model_name == custom_model

    @pytest.mark.asyncio
    async def test_embed_without_init_raises_error(self):
        """Test that embed raises error if model not initialized"""
        service = EmbeddingService()

        with pytest.raises(RuntimeError) as exc:
            await service.embed(["test"])

        assert "Embedding model is not loaded" in str(exc.value)

    @pytest.mark.asyncio
    async def test_init_uses_asyncio_to_thread(self):
        """Test that init uses asyncio.to_thread for model loading"""
        with (
            patch(
                "insightvault.services.embedding.asyncio.to_thread"
            ) as mock_to_thread,
            patch(
                "insightvault.services.embedding.SentenceTransformer"
            ) as mock_transformer,
        ):
            mock_to_thread.return_value = mock_transformer.return_value
            service = EmbeddingService()

            await service.init()

            mock_to_thread.assert_called_once_with(mock_transformer, "all-MiniLM-L6-v2")
