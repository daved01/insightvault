import asyncio
from abc import ABC, abstractmethod
from logging import Logger

from ollama import AsyncClient, ChatResponse

from ..utils.logging import get_logger


class LLMService(ABC):
    @abstractmethod
    def __init__(self) -> None:
        """Initialize the LLM service"""

    @abstractmethod
    async def query(self, prompt: str) -> str | None:
        """Generate a one-off response from the model without chat history."""

    @abstractmethod
    async def chat(self, prompt: str) -> str | None:
        """Generate a response from the model while maintaining chat history."""

    @abstractmethod
    def clear_chat_history(self) -> None:
        """Clear the chat history."""


class OllamaLLMService(LLMService):
    """Ollama LLM service"""

    def __init__(self, model_name: str = "llama3") -> None:
        self.logger: Logger = get_logger("insightvault.services.llm")
        self.model_name = model_name
        self.client: AsyncClient | None = None  # AsyncClient()
        self.chat_history: list[dict[str, str]] = []
        self.loading_task: asyncio.Task[None] = asyncio.create_task(self._load_model())

    def clear_chat_history(self) -> None:
        """Clear the chat history."""
        self.chat_history = []

    async def _load_model(self) -> None:
        """Load the embedding model"""
        self.logger.debug(f"Loading llm: {self.model_name}")
        self.client = AsyncClient()
        self.logger.debug("LLM loaded!")

    async def get_client(self) -> AsyncClient:
        if self.client is None:
            self.logger.debug("LLM not loaded, waiting for loading task to complete")
            await self.loading_task

        # Better safe than sorry (and for mypy)
        if self.client is None:
            raise RuntimeError("Client is not loaded!")
        return self.client

    async def query(self, prompt: str) -> str | None:
        """Generate a one-off response from the model without chat history."""
        if not self.client:
            self.client = await self.get_client()
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
        self.chat_history.append({"role": "user", "content": prompt})
        if not self.client:
            self.client = await self.get_client()
        response: str | None = await self.query(prompt)
        if response is None:
            return "Error: No response from the model."
        self.chat_history.append({"role": "assistant", "content": response})
        return response
