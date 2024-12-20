import asyncio

from ..models.document import Document
from ..services.database import ChromaDatabaseService
from ..services.embedding import EmbeddingService
from ..services.splitter import SplitterService
from ..utils.logging import get_logger


class BaseApp:
    def __init__(self, name: str = "insightvault.app") -> None:
        self.name = name
        self.logger = get_logger(name)
        self.db = ChromaDatabaseService()
        self.splitter = SplitterService()
        self.embedder: EmbeddingService | None = None

    async def init_base(self) -> None:
        """Initialize the app"""
        self.logger.debug(f"Initializing BaseApp `{self.name}` ...")
        self.embedder = EmbeddingService()
        await self.embedder.get_client()
        self.logger.debug(f"BaseApp `{self.name}` initialized!")

    def add_documents(self, documents: list[Document]) -> None:
        """Add documents to the database"""
        self.logger.debug("Adding document(s)")
        return asyncio.get_event_loop().run_until_complete(
            self.async_add_documents(documents)
        )

    async def async_add_documents(self, documents: list[Document]) -> None:
        """Async version of add_document"""
        self.logger.debug("Async adding document(s)")

        if not self.embedder:
            raise RuntimeError("Embedding service is not loaded!")

        processed_documents = []
        for doc in documents:
            # Split document into chunks
            chunks: list[Document] = self.splitter.split(doc)

            # Get embeddings for the chunk contents
            chunk_contents = [chunk.content for chunk in chunks]
            embeddings = self.embedder.embed(chunk_contents)

            # Add embeddings to chunks
            for chunk, embedding in zip(chunks, embeddings, strict=True):  # type: ignore
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
        return await self.db.delete_all_documents()

    def list_documents(self) -> list[Document] | None:
        """List all documents in the database"""
        self.logger.debug("Listing all documents ...")
        return asyncio.get_event_loop().run_until_complete(self.async_list_documents())

    async def async_list_documents(self) -> list[Document] | None:
        """Async version of list_documents"""
        self.logger.debug("Async listing all documents ...")
        return await self.db.get_documents()
