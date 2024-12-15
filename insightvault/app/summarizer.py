import asyncio

from ..models.document import Document
from .base import BaseApp


class SummarizerApp(BaseApp):
    """Summarizer application

    This application is used to summarize documents.
    """

    def __init__(self, name: str = "insightvault") -> None:
        super().__init__(name)

    def summarize(self, documents: list[Document]) -> str:
        """Summarize a list of documents"""
        self.logger.info("Summarizing document(s)")
        return asyncio.get_event_loop().run_until_complete(
            self.async_summarize(documents)
        )

    async def async_summarize(self, documents: list[Document]) -> str:
        """Async version of summarize"""
        self.logger.info("Async summarizing document(s)")
        return "\n".join([doc.content for doc in documents])
