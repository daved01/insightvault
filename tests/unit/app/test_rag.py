from unittest.mock import AsyncMock, Mock, patch

import pytest

from insightvault.app.rag import RAGApp
from insightvault.models.document import Document
from tests.unit import BaseTest
from tests.unit.app.test_base import TestBaseApp


class TestRAGApp(TestBaseApp, BaseTest):
    @pytest.fixture
    def mock_llm_service(self):
        """Create a mock LLM service"""
        service = AsyncMock()
        service.query = AsyncMock(return_value="Generated response")
        service.get_client = AsyncMock()
        return service

    @pytest.fixture
    def mock_prompt_service(self):
        """Create a mock prompt service"""
        service = Mock()
        service.get_prompt.return_value = "Generated prompt text"
        return service

    @pytest.fixture
    def rag_app(
        self,
        mock_db_service,
        mock_splitter_service,
        mock_embedding_service,
        mock_llm_service,
        mock_prompt_service,
    ):
        """Create a RAG app with mocked services"""
        with (
            patch("insightvault.app.base.ChromaDatabaseService") as mock_db_class,
            patch("insightvault.app.base.SplitterService") as mock_splitter_class,
            patch("insightvault.app.base.EmbeddingService") as mock_embedding_class,
            patch("insightvault.app.rag.OllamaLLMService") as mock_llm_class,
            patch("insightvault.app.rag.PromptService") as mock_prompt_class,
        ):
            mock_db_class.return_value = mock_db_service
            mock_splitter_class.return_value = mock_splitter_service
            mock_embedding_class.return_value = mock_embedding_service
            mock_llm_class.return_value = mock_llm_service
            mock_prompt_class.return_value = mock_prompt_service

            app = RAGApp()
            return app

    @pytest.mark.asyncio
    async def test_async_query_generates_response(self, rag_app, sample_documents):
        """Test that query retrieves documents and generates response"""
        # Setup mock responses
        rag_app.embedder.embed.return_value = [[0.1, 0.2, 0.3]]
        rag_app.db.query.return_value = sample_documents

        # Initialize RAG app
        await rag_app.init_rag()

        result = await rag_app.async_query("test query")

        # Verify initialization was called
        rag_app.llm.get_client.assert_called_once()

        # Verify embeddings were generated
        rag_app.embedder.embed.assert_called_once_with(["test query"])

        # Verify database was queried with embeddings
        rag_app.db.query.assert_called_once_with([0.1, 0.2, 0.3])

        # Verify prompt was generated with correct context
        expected_context = "Content from first document\nContent from second document"
        rag_app.prompt_service.get_prompt.assert_called_once_with(
            prompt_type="rag_context",
            context={"question": "test query", "context": expected_context},
        )

        # Verify LLM was called with prompt
        rag_app.llm.query.assert_called_once_with(prompt="Generated prompt text")

        assert result == "Generated response"

    def test_sync_query_calls_async_version(self, rag_app):
        """Test that sync query method properly calls async version"""
        with patch("asyncio.get_event_loop") as mock_loop:
            mock_loop.return_value.run_until_complete = Mock()

            rag_app.query("test query")

            mock_loop.return_value.run_until_complete.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_query_with_no_results(self, rag_app):
        """Test query behavior when no documents are found"""
        rag_app.embedder.embed.return_value = [[0.1, 0.2, 0.3]]
        rag_app.db.query.return_value = []

        # Initialize RAG app
        await rag_app.init_rag()

        result = await rag_app.async_query("test query")

        assert result == "No documents found in the database."

    @pytest.mark.asyncio
    async def test_async_query_preserves_question(self, rag_app):
        """Test that original question is preserved in prompt generation"""
        complex_query = "What is the meaning of life?"
        rag_app.embedder.embed.return_value = [[0.1, 0.2, 0.3]]
        rag_app.db.query.return_value = []

        await rag_app.async_query(complex_query)

        rag_app.prompt_service.get_prompt.assert_called_once_with(
            prompt_type="rag_context",
            context={"question": complex_query, "context": ""},
        )

    @pytest.mark.asyncio
    async def test_async_query_joins_contexts_correctly(self, rag_app):
        """Test that document contents are properly joined into context"""
        docs = [
            Document(title="Doc 1", content="First line.\nSecond line."),
            Document(title="Doc 2", content="Third line.\nFourth line."),
        ]
        rag_app.embedder.embed.return_value = [[0.1, 0.2, 0.3]]
        rag_app.db.query.return_value = docs

        await rag_app.async_query("test query")

        expected_context = "First line.\nSecond line.\nThird line.\nFourth line."
        rag_app.prompt_service.get_prompt.assert_called_once_with(
            prompt_type="rag_context",
            context={"question": "test query", "context": expected_context},
        )

    @pytest.mark.asyncio
    async def test_init_rag_initializes_services(self, rag_app):
        """Test that init_rag properly initializes all services"""
        await rag_app.init_rag()

        # Verify base services were initialized
        rag_app.db.init_db.assert_called_once()
        rag_app.embedder.get_model.assert_called_once()

        # Verify RAG-specific services were initialized
        rag_app.llm.get_client.assert_called_once()
