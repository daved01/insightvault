import pytest

from insightvault.services.prompt import PromptService


class TestPromptService:
    @pytest.fixture
    def prompt_service(self):
        return PromptService()

    def test_get_prompt_summarize_text(self, prompt_service):
        """Test getting summarize text prompt with context"""
        context = {"text": "Sample text to summarize"}
        prompt = prompt_service.get_prompt("summarize_text", context)

        assert "Sample text to summarize" in prompt
        assert "Text to summarize:" in prompt
        assert "Make the summary concise" in prompt

    def test_get_prompt_rag_context(self, prompt_service):
        """Test getting RAG context prompt with context"""
        context = {
            "question": "What is Python?",
            "context": "Python is a programming language.",
        }
        prompt = prompt_service.get_prompt("rag_context", context)

        assert "What is Python?" in prompt
        assert "Python is a programming language." in prompt
        assert "Question:" in prompt
        assert "Context:" in prompt

    def test_get_prompt_without_context(self, prompt_service):
        """Test getting prompt without context"""
        prompt = prompt_service.get_prompt("summarize_text")
        assert "{text}" in prompt
        assert "Text to summarize:" in prompt

    def test_get_prompt_invalid_type(self, prompt_service):
        """Test getting prompt with invalid type raises ValueError"""
        with pytest.raises(ValueError) as exc:
            prompt_service.get_prompt("invalid_type")
        assert "Prompt for key 'invalid_type' not found" in str(exc.value)

    def test_get_prompt_missing_context_variable(self, prompt_service):
        """Test getting prompt with missing context variable raises KeyError"""
        with pytest.raises(KeyError):
            prompt_service.get_prompt("summarize_text", {"invalid_key": "value"})
