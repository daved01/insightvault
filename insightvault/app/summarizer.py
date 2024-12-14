from .base import BaseApp
from ..models.document import Document
import asyncio


class SummarizerApp(BaseApp):
    """Summarizer application

    This application is used to summarize documents.
    """
    def __init__(self, name: str = "insightvault") -> None:
        super().__init__(name)

    def summarize(self, documents: list[Document]) -> str:
        """Summarize a document or a list of documents"""
        self.logger.info("Summarizing documents ...")
        return asyncio.get_event_loop().run_until_complete(self.async_summarize(documents))
        
    async def async_summarize(self, documents: list[Document]) -> str:
        """Async version of summarize"""
        self.logger.info("Async summarizing documents ...")
        return "\n".join([doc.content for doc in documents])
