import asyncio

from ..models.document import Document
from .base import BaseApp


class SearchApp(BaseApp):
    """Search application for semantic search

    This application is used to query the database and add documents to the database.

    Attributes:
        db (Database): The database service.
    """

    def __init__(self, name: str = "insightvault.app.search") -> None:
        super().__init__(name)

    def query(self, query: str) -> list[str]:
        """Query the database for documents similar to the query.

        Returns an alphabetically sorted list of document titles.
        """
        self.logger.debug(f"Querying the database for: {query}")
        return asyncio.get_event_loop().run_until_complete(self.async_query(query))

    async def async_query(self, query: str) -> list[str]:
        """Async version of query"""
        self.logger.debug(f"Async querying the database for: {query}")
        await self.init()
        query_embeddings: list[list[float]] = await self.embedder.embed([query])
        response: list[Document] = await self.db.query(query_embeddings[0])
        return sorted(set(doc.title for doc in response))
