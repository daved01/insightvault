import asyncio

from ..services.llm import OllamaLLMService
from .base import BaseApp


class SummarizerApp(BaseApp):
    """Summarizer application

    This application is used to summarize documents.
    """

    def __init__(self, name: str = "insightvault") -> None:
        super().__init__(name)
        self.llm = OllamaLLMService()

    def summarize(self, text: str) -> str:
        """Summarize a list of documents"""
        self.logger.info("Summarizing document(s)")
        return asyncio.get_event_loop().run_until_complete(
            self.async_summarize(text=text)
        )

    async def async_summarize(self, text: str) -> str:
        """Async version of summarize"""
        self.logger.info("Async summarizing document(s)")
        response = await self.llm.query(prompt=text)
        return f"Respose:\n`{response}`"
