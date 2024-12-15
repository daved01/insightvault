from abc import ABC, abstractmethod

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


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


# TODO: Find solution to the weights issue
class MistralLLMService(LLMService):
    def __init__(self, api_key: str):
        """
        Initialize the Mistral LLM using Mistral's API directly.

        Args:
            api_key (str): Your Mistral API key
        """
        print("🔄 Initializing Mistral client...")
        self.client = MistralClient(api_key=api_key)
        self.chat_history: list[ChatMessage] = []
        print("✅ Client initialized successfully!")
