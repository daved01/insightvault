import asyncio
from abc import ABC, abstractmethod
from logging import Logger

from ollama import AsyncClient, ChatResponse

from ..utils.logging import get_logger


class AbstractLLMService(ABC):
    @abstractmethod
    def __init__(self, model_name: str) -> None:
        """
        Configure the LLM service with the necessary settings.

        Args:
            model_name (str): The name of the model to use.
        """

    @abstractmethod
    async def init(self) -> None:
        """
        Prepare the LLM service for use, such as loading model weights.
        """

    @abstractmethod
    async def query(self, prompt: str) -> str | None:
        """Generate a one-off response from the model without chat history."""

    @abstractmethod
    async def chat(self, prompt: str) -> str | None:
        """Generate a response from the model while maintaining chat history."""

    @abstractmethod
    async def clear_chat_history(self) -> None:
        """Clear the chat history."""


class BaseLLMService(AbstractLLMService):
    def __init__(self, model_name: str) -> None:
        """
        Configure base properties for the LLM service.

        Args:
            model_name (str): The name of the model to use.
        """
        self.logger: Logger = get_logger("insightvault.services.llm")
        self.model_name: str = model_name
        self.chat_history: list[dict[str, str]] = []


class OllamaLLMService(BaseLLMService):
    """Ollama LLM service"""

    def __init__(self, model_name: str = "llama3") -> None:
        super().__init__(model_name)
        self.client: AsyncClient | None = None

    async def init(self) -> None:
        """Initialize the LLM service"""
        self.client = await asyncio.to_thread(AsyncClient)
        self.logger.debug(f"LLM loaded `{self.model_name}`!")

    async def clear_chat_history(self) -> None:
        """Clear the chat history."""
        self.chat_history = []

    async def query(self, prompt: str) -> str | None:
        """Generate a one-off response from the model without chat history."""
        if not self.client:
            raise RuntimeError("LLM client is not loaded! Call `init()` first.")

        response: ChatResponse = await self.client.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return response.message.content

    async def chat(self, prompt: str) -> str | None:
        """Generate a response from the model while maintaining chat history."""
        if not self.client:
            raise RuntimeError("LLM client is not loaded! Call `init()` first.")

        self.chat_history.append({"role": "user", "content": prompt})

        response: str | None = await self.query(prompt)
        if response is None:
            return "Error: No response from the model."
        self.chat_history.append({"role": "assistant", "content": response})
        return response
