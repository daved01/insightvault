from abc import ABC, abstractmethod

from ollama import AsyncClient, ChatResponse


class LLMService(ABC):
    @abstractmethod
    def __init__(self) -> None:
        """Initialize the LLM service"""

    @abstractmethod
    def query(self, prompt: str) -> str:
        """Generate a one-off response from the model without chat history."""

    @abstractmethod
    def chat(self, prompt: str) -> str:
        """Generate a response from the model while maintaining chat history."""

    @abstractmethod
    def clear_chat_history(self) -> None:
        """Clear the chat history."""


class OllamaLLMService(LLMService):
    """Ollama LLM service"""

    def __init__(self, model: str = "llama3") -> None:
        self.model = model
        self.chat_history: list[str] = []
        self.client = AsyncClient()

    def clear_chat_history(self) -> None:
        """Clear the chat history."""
        self.chat_history = []

    async def query(self, prompt: str) -> str:
        """Generate a one-off response from the model without chat history."""
        response: ChatResponse = await self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return response.message.content

    async def chat(self, prompt: str) -> str:
        """Generate a response from the model while maintaining chat history."""
        self.chat_history.append({"role": "user", "content": prompt})
        response: ChatResponse = await self.query(prompt)
        self.chat_history.append({"role": "assistant", "content": response})
        return response
