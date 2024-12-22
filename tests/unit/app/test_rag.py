from unittest.mock import AsyncMock, Mock, patch

import pytest

from insightvault.app.rag import RAGApp
from insightvault.models.document import Document
from tests.unit.app.test_base import BaseAppTestSetup


class TestRAGApp(BaseAppTestSetup):
    @pytest.fixture
    def mock_llm_service(self):
        """Create a mock LLM service"""
        service = AsyncMock()
        service.init = AsyncMock()
        service.query = AsyncMock(return_value="Generated response")
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
    async def test_init_initializes_services(self, rag_app):
        """Test that init initializes all required services"""
        await rag_app.init()

        rag_app.llm_service.init.assert_called_once()
        rag_app.embedder_service.init.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_query_generates_response(self, rag_app):
        """Test that query retrieves documents and generates response"""
        # Setup mock responses
        await rag_app.init()
        rag_app.embedder_service.embed.return_value = [[0.1, 0.2, 0.3]]
        rag_app.db_service.query.return_value = [
            Document(title="Doc 1", content="Content from first document"),
            Document(title="Doc 2", content="Content from second document"),
        ]

        result = await rag_app.async_query("test query")

        # Verify embeddings were generated
        rag_app.embedder_service.embed.assert_called_once_with(["test query"])

        # Verify database was queried with embeddings
        rag_app.db_service.query.assert_called_once_with([0.1, 0.2, 0.3])

        # Verify prompt was generated with correct context
        expected_context = "Content from first document\nContent from second document"
        rag_app.prompt_service.get_prompt.assert_called_once_with(
            prompt_type="rag_context",
            context={"question": "test query", "context": expected_context},
        )

        # Verify LLM was called with prompt
        rag_app.llm_service.query.assert_called_once_with(
            prompt="Generated prompt text"
        )

        assert result == ["Generated response"]

    def test_sync_query_calls_async_version(self, rag_app):
        """Test that sync query method properly calls async version"""
        with patch("asyncio.run") as mock_run:
            rag_app.query("test query")
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_query_with_no_results(self, rag_app):
        """Test query behavior when no documents are found"""
        await rag_app.init()
        rag_app.embedder_service.embed.return_value = [[0.1, 0.2, 0.3]]
        rag_app.db_service.query.return_value = None

        result = await rag_app.async_query("test query")

        assert result == ["No documents found in the database."]

    @pytest.mark.asyncio
    async def test_async_query_with_llm_no_response(self, rag_app):
        """Test handling of no response from LLM"""
        await rag_app.init()
        rag_app.embedder_service.embed.return_value = [[0.1, 0.2, 0.3]]
        rag_app.db_service.query.return_value = [
            Document(title="Doc", content="Content")
        ]
        rag_app.llm_service.query.return_value = None

        result = await rag_app.async_query("test query")

        assert result == ["No response from the LLM."]

    @pytest.mark.asyncio
    async def test_async_query_without_embedder(self, rag_app):
        """Test query fails when embedder is not initialized"""
        await rag_app.init()
        rag_app.embedder_service = None

        with pytest.raises(RuntimeError) as exc:
            await rag_app.async_query("test query")

        assert "Embedding service is not loaded" in str(exc.value)

    @pytest.mark.asyncio
    async def test_async_query_without_db(self, rag_app):
        """Test query fails when database is not initialized"""
        await rag_app.init()
        rag_app.db_service = None

        with pytest.raises(RuntimeError) as exc:
            await rag_app.async_query("test query")

        assert "Database service is not loaded" in str(exc.value)
