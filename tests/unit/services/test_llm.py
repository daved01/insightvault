from unittest.mock import AsyncMock

import pytest

from insightvault.services.llm import OllamaLLMService


class TestOllamaLLMService:
    @pytest.fixture
    def mock_chat_response(self):
        """Mock chat response from Ollama"""

        class MockMessage:
            content = "This is a mock response"

        class MockResponse:
            message = MockMessage()

        return MockResponse()

    @pytest.fixture
    def llm_service(self):
        """Create LLM service with mocked client"""
        service = OllamaLLMService(model="test-model")
        service.client = AsyncMock()
        service.client.chat.side_effect = [None]
        return service

    @pytest.mark.asyncio
    async def test_query_returns_response(self, llm_service, mock_chat_response):
        """Test that query returns the expected response"""
        llm_service.client.chat.side_effect = [mock_chat_response]

        response = await llm_service.query("Test prompt")

        assert response == "This is a mock response"
        llm_service.client.chat.assert_called_once_with(
            model="test-model",
            messages=[{"role": "user", "content": "Test prompt"}],
        )

    @pytest.mark.asyncio
    async def test_chat_maintains_history(self, llm_service, mock_chat_response):
        """Test that chat maintains conversation history"""
        llm_service.client.chat.side_effect = [mock_chat_response]

        response = await llm_service.chat("Test prompt")

        assert response == "This is a mock response"
        assert len(llm_service.chat_history) == 2
        assert llm_service.chat_history[0] == {"role": "user", "content": "Test prompt"}
        assert llm_service.chat_history[1] == {
            "role": "assistant",
            "content": "This is a mock response",
        }

    def test_clear_chat_history(self, llm_service):
        """Test that clear_chat_history removes all history"""
        llm_service.chat_history = [
            {"role": "user", "content": "test"},
            {"role": "assistant", "content": "response"},
        ]

        llm_service.clear_chat_history()

        assert len(llm_service.chat_history) == 0

    @pytest.mark.asyncio
    async def test_chat_with_multiple_turns(self, llm_service, mock_chat_response):
        """Test multiple turns of conversation"""

        llm_service.client.chat.side_effect = [
            mock_chat_response,
            mock_chat_response,
        ]

        await llm_service.chat("First prompt")
        await llm_service.chat("Second prompt")

        assert len(llm_service.chat_history) == 4
        assert llm_service.chat_history[0]["content"] == "First prompt"
        assert llm_service.chat_history[2]["content"] == "Second prompt"

    @pytest.mark.asyncio
    async def test_query_with_different_model(self, mock_chat_response):
        """Test query with a different model"""
        service = OllamaLLMService(model="different-model")
        service.client = AsyncMock()
        service.client.chat.return_value = mock_chat_response

        await service.query("Test prompt")

        service.client.chat.assert_called_once_with(
            model="different-model",
            messages=[{"role": "user", "content": "Test prompt"}],
        )
