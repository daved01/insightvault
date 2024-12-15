import asyncio

from ..models.document import Document
from ..services.database import DatabaseService
from ..services.embedding import EmbeddingService
from ..services.splitter import SplitterService
from .base import BaseApp


class RAGApp(BaseApp):
    """RAG application

    This application is used to query the database and add documents to the database.

    Attributes:
        db (Database): The database service.
    """

    def __init__(self, name: str = "insightvault") -> None:
        super().__init__(name)
        self.db = DatabaseService()
        self.splitter = SplitterService()
        self.embedder = EmbeddingService()

    def query(self, query: str | list[str]) -> list[Document]:
        """Query the database for documents similar to the query"""
        self.logger.debug(f"Querying the database for: {query}")
        return asyncio.get_event_loop().run_until_complete(self.async_query(query))

    async def async_query(self, query: str | list[str]) -> list[Document]:
        """Async version of query"""
        self.logger.debug(f"Async querying the database for: {query}")
        return await self.db.query(query)

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

            # Get embeddings for chunks
            embedded_chunks: list[Document] = self.embedder.embed(chunks)

            # Create new documents with chunks and embeddings
            processed_documents.extend(embedded_chunks)

        # Add processed documents to db
        return await self.db.add_documents(processed_documents)

    def delete_documents(self, document_ids: str | list[str]) -> None:
        """Delete a document from the database"""
        self.logger.debug("Deleting document(s)")
        return asyncio.get_event_loop().run_until_complete(
            self.async_delete_documents(document_ids)
        )

    async def async_delete_documents(self, document_ids: str | list[str]) -> None:
        """Async version of delete_documents"""
        self.logger.debug("Async deleting document(s)")
        return await self.db.delete_documents(document_ids)

    def delete_all_documents(self) -> None:
        """Delete all documents from the database"""
        self.logger.debug("Deleting all documents ...")
        return asyncio.get_event_loop().run_until_complete(
            self.async_delete_all_documents()
        )

    async def async_delete_all_documents(self) -> None:
        """Async version of delete_all_documents"""
        self.logger.debug("Async deleting all documents ...")
        return await self.db.delete_all_documents()

    def list_documents(self) -> list[Document]:
        """List all documents in the database"""
        self.logger.debug("Listing all documents ...")
        return asyncio.get_event_loop().run_until_complete(self.async_list_documents())

    async def async_list_documents(self) -> list[Document]:
        """Async version of list_documents"""
        self.logger.debug("Async listing all documents ...")
        return await self.db.list_documents()
