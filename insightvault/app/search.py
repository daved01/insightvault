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

    async def init(self) -> None:
        """Initialize the search app"""
        await super().init()
        self.logger.debug(f"SearchApp `{self.name}` initialized!")

    def query(self, query: str) -> list[str]:
        """Query the database for documents similar to the query.

        Returns an alphabetically sorted list of document titles.
        """
        return asyncio.run(self.async_query(query))

    async def async_query(self, query: str) -> list[str]:
        """Async version of query"""
        self.logger.debug(f"Querying the database for: {query}")
        await self.init()
        if not self.embedder_service:
            raise RuntimeError("Embedding service is not loaded!")
        query_embeddings: list[list[float]] = await self.embedder_service.embed([query])
        response: list[Document] = await self.db_service.query(query_embeddings[0])
        return sorted(set(doc.title for doc in response))
