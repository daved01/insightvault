from .base import BaseApp
from ..models.document import Document
import asyncio
from ..services import ensure_list
from typing import Union, List


class SummarizerApp(BaseApp):
    """Summarizer application

    This application is used to summarize documents.
    """
    def __init__(self, name: str = "insightvault") -> None:
        super().__init__(name)

    @ensure_list(arg_name='documents')
    def summarize(self, documents: Union[Document, List[Document]]) -> str:
        """Summarize one or more documents"""
        self.logger.info("Summarizing document(s)")
        return asyncio.get_event_loop().run_until_complete(self.async_summarize(documents))
        
    @ensure_list(arg_name='documents')
    async def async_summarize(self, documents: Union[Document, List[Document]]) -> str:
        """Async version of summarize"""
        self.logger.info("Async summarizing document(s)")
        return "\n".join([doc.content for doc in documents])
