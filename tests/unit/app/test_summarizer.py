from unittest.mock import AsyncMock, Mock, patch

import pytest

from insightvault.app.summarizer import SummarizerApp
from tests.unit.app.test_base import BaseAppTestSetup


class TestSummarizerApp(BaseAppTestSetup):
    @pytest.fixture
    def mock_llm_service(self):
        """Create a mock LLM service"""
        service = AsyncMock()
        service.query = AsyncMock(return_value="Summarized text")
        return service

    @pytest.fixture
    def mock_prompt_service(self):
        """Create a mock prompt service"""
        service = Mock()
        service.get_prompt.return_value = "Generated prompt text"
        return service

    @pytest.fixture
    def summarizer_app(
        self,
        mock_db_service,
        mock_splitter_service,
        mock_embedding_service,
        mock_llm_service,
        mock_prompt_service,
    ):
        """Create a summarizer app with mocked services"""
        with (
            patch("insightvault.app.base.ChromaDatabaseService") as mock_db_class,
            patch("insightvault.app.base.SplitterService") as mock_splitter_class,
            patch("insightvault.app.base.EmbeddingService") as mock_embedding_class,
            patch("insightvault.app.summarizer.OllamaLLMService") as mock_llm_class,
            patch("insightvault.app.summarizer.PromptService") as mock_prompt_class,
        ):
            mock_db_class.return_value = mock_db_service
            mock_splitter_class.return_value = mock_splitter_service
            mock_embedding_class.return_value = mock_embedding_service
            mock_llm_class.return_value = mock_llm_service
            mock_prompt_class.return_value = mock_prompt_service

            app = SummarizerApp()
            return app

    @pytest.mark.asyncio
    async def test_async_summarize_generates_summary(self, summarizer_app):
        """Test that summarize generates a summary using LLM"""
        text = "Text to summarize"
        result = await summarizer_app.async_summarize(text)

        # Verify prompt was generated
        summarizer_app.prompt_service.get_prompt.assert_called_once_with(
            prompt_type="summarize_text",
            context={"text": text},
        )

        # Verify LLM was called with prompt
        summarizer_app.llm_service.query.assert_called_once_with(
            prompt="Generated prompt text"
        )

        assert result == "Summarized text"

    @pytest.mark.asyncio
    async def test_async_summarize_preserves_text(self, summarizer_app):
        """Test that original text is preserved in prompt generation"""
        complex_text = "This is a complex text\nwith multiple lines\nand special chars!"
        await summarizer_app.async_summarize(complex_text)

        summarizer_app.prompt_service.get_prompt.assert_called_once_with(
            prompt_type="summarize_text",
            context={"text": complex_text},
        )

    @pytest.mark.asyncio
    async def test_async_summarize_with_empty_text(self, summarizer_app):
        """Test summarization of empty text"""
        result = await summarizer_app.async_summarize("")

        summarizer_app.prompt_service.get_prompt.assert_called_once_with(
            prompt_type="summarize_text",
            context={"text": ""},
        )
        assert result == "Summarized text"  # Based on mock response

    @pytest.mark.asyncio
    async def test_async_summarize_handles_none_response(self, summarizer_app):
        """Test handling of None response from LLM"""
        summarizer_app.llm_service.query.return_value = None

        result = await summarizer_app.async_summarize("Test text")

        assert result is None

    @pytest.mark.asyncio
    async def test_async_summarize_with_long_text(self, summarizer_app):
        """Test summarization of long text"""
        long_text = " ".join(["test"] * 1000)  # Create a long text
        await summarizer_app.async_summarize(long_text)

        summarizer_app.prompt_service.get_prompt.assert_called_once_with(
            prompt_type="summarize_text",
            context={"text": long_text},
        )
