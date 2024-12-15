import asyncio

from ..models.document import Document
from ..services.database import ChromaDatabaseService
from ..services.embedding import EmbeddingService
from ..services.splitter import SplitterService
from .base import BaseApp


class SearchApp(BaseApp):
    """Search application for semantic search

    This application is used to query the database and add documents to the database.

    Attributes:
        db (Database): The database service.
    """

    def __init__(self, name: str = "insightvault.app.search") -> None:
        super().__init__(name)
        self.db = ChromaDatabaseService()
        self.splitter = SplitterService()
        self.embedder = EmbeddingService()

    def query(self, query: str) -> list[str]:
        """Query the database for documents similar to the query.

        Returns an alphabetically sorted list of document titles.
        """
        self.logger.debug(f"Querying the database for: {query}")
        return asyncio.get_event_loop().run_until_complete(self.async_query(query))

    # TODO: This does not work well because of the database currently.
    async def async_query(self, query: str) -> list[str]:
        """Async version of query"""
        self.logger.debug(f"Async querying the database for: {query}")

        query_embeddings: list[list[float]] = self.embedder.embed([query])
        response: list[Document] = await self.db.query(query_embeddings[0])
        return sorted(set(doc.title for doc in response))

    def add_documents(self, documents: list[Document]) -> None:
        """Add documents to the database"""
        self.logger.debug("Adding document(s)")
        return asyncio.get_event_loop().run_until_complete(
            self.async_add_documents(documents)
        )

    async def async_add_documents(self, documents: list[Document]) -> None:
        """Async version of add_document"""
        self.logger.debug("Async adding document(s)")

        processed_documents = []
        for doc in documents:
            # Split document into chunks
            chunks: list[Document] = self.splitter.split(doc)

            # Get embeddings for the chunk contents
            chunk_contents = [chunk.content for chunk in chunks]
            embeddings = self.embedder.embed(chunk_contents)

            # Add embeddings to chunks
            for chunk, embedding in zip(chunks, embeddings, strict=True):
                chunk.embedding = embedding
                processed_documents.append(chunk)

        # Add processed documents to db
        return await self.db.add_documents(processed_documents)

    def delete_all_documents(self) -> None:
        """Delete all documents from the database"""
        self.logger.debug("Deleting all documents ...")
        return asyncio.get_event_loop().run_until_complete(
            self.async_delete_all_documents()
        )

    async def async_delete_all_documents(self) -> None:
        """Async version of delete_all_documents"""
        self.logger.debug("Async deleting all documents ...")
        # TODO: Implement async delete_all_documents
        return await self.db.delete_all_documents()

    def list_documents(self) -> list[Document] | None:
        """List all documents in the database"""
        self.logger.debug("Listing all documents ...")
        return asyncio.get_event_loop().run_until_complete(self.async_list_documents())

    async def async_list_documents(self) -> list[Document] | None:
        """Async version of list_documents"""
        self.logger.debug("Async listing all documents ...")
        return await self.db.get_documents()
