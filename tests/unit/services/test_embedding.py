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
    def embedding_service(self):
        """Create embedding service with mocked client"""
        service = EmbeddingService(model_name="test-model")
        service.client = Mock()
        return service

    @patch("insightvault.services.embedding.SentenceTransformer")
    def test_init_creates_model(self, mock_transformer):
        """Test that init creates the model correctly"""
        service = EmbeddingService(model_name="test-model")

        mock_transformer.assert_called_once_with("test-model")
        assert service.client == mock_transformer.return_value

    @pytest.fixture
    def mock_sentence_transformer(self):
        """Create mock SentenceTransformer"""
        mock_client = Mock()
        mock_client.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        return mock_client

    @patch("insightvault.services.embedding.SentenceTransformer")
    def test_embed_returns_list_of_embeddings(self, embedding_service, mock_embeddings):
        """Test that embed returns correct format"""
        embedding_service.client.encode.return_value = mock_embeddings
        texts = ["First text", "Second text"]

        result = embedding_service.embed(texts)

        assert isinstance(result, list)
        expected_embeddings_count = 2
        assert len(result) == expected_embeddings_count
        assert isinstance(result[0], list)
        assert result[0] == [0.1, 0.2, 0.3]
        assert result[1] == [0.4, 0.5, 0.6]

    @patch("insightvault.services.embedding.SentenceTransformer")
    def test_embed_calls_encode_with_correct_params(self, mock_transformer):
        """Test that embed calls encode with correct parameters"""
        # Setup
        mock_client = Mock()
        mock_client.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        mock_transformer.return_value = mock_client

        service = EmbeddingService(model_name="test-model")
        texts = ["Test text"]

        # Execute
        result = service.embed(texts)

        # Verify
        mock_client.encode.assert_called_once_with(
            texts, batch_size=32, show_progress_bar=False, convert_to_numpy=True
        )
        assert result == [[0.1, 0.2, 0.3]]

    def test_embed_with_multiple_texts(self, embedding_service, mock_embeddings):
        """Test embedding multiple texts"""
        embedding_service.client.encode.return_value = mock_embeddings
        texts = ["First text", "Second text"]

        result = embedding_service.embed(texts)

        assert len(result) == len(texts)
        embedding_service.client.encode.assert_called_once()

    def test_embed_with_empty_list(self, embedding_service):
        """Test embedding empty list of texts"""
        embedding_service.client.encode.return_value = np.array([])

        result = embedding_service.embed([])

        assert result == []
        embedding_service.client.encode.assert_called_once_with(
            [], batch_size=32, show_progress_bar=False, convert_to_numpy=True
        )

    def test_custom_model_name(self):
        """Test service initialization with custom model name"""
        custom_model = "custom-bert-model"
        service = EmbeddingService(model_name=custom_model)

        assert service.model_name == custom_model
