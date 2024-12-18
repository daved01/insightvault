from abc import ABC, abstractmethod

import chromadb
from chromadb.config import Settings

from ..constants import COSINE_SIMILARITY_METADATA, DEFAULT_COLLECTION_NAME
from ..models.document import Document
from ..utils.logging import get_logger


class AbstractDatabaseService(ABC):
    """Abstract database service"""

    @abstractmethod
    async def init(self) -> None:
        """Initialize the database"""
        pass

    @abstractmethod
    async def add_documents(self, documents: list[Document]) -> None:
        """Add a list of documents to the database"""
        pass

    @abstractmethod
    async def query(self, query_embedding: list[float]) -> list[Document]:
        """Query the database for documents similar to the query embedding"""
        pass

    @abstractmethod
    async def get_documents(self) -> list[Document]:
        """Get all documents from the database"""
        pass

    @abstractmethod
    async def delete_all_documents(self) -> None:
        """Delete all documents from the database"""
        pass


class ChromaDatabaseService(AbstractDatabaseService):
    """Chroma database service

    This service is used to interact with the Chroma database.

    Embedding functions are not provided here, so the caller must provide them.
    """

    def __init__(
        self,
        persist_directory: str = "data/.db",
    ):
        self.logger = get_logger("insightvault.services.database")
        self.persist_directory = persist_directory
        self.client = None

    async def init(self) -> None:
        """Initialize the database"""

        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )
        self.logger.debug("Database initialized")

    async def add_documents(
        self, documents: list[Document], collection: str = DEFAULT_COLLECTION_NAME
    ) -> None:
        """Add a list of documents to the database. The documents must have embeddings."""
        if not self.client:
            await self.init()

        collection = self.client.get_or_create_collection(
            name=collection, metadata=COSINE_SIMILARITY_METADATA
        )

        collection.add(
            documents=[doc.content for doc in documents],
            metadatas=[doc.metadata for doc in documents],
            embeddings=[doc.embedding for doc in documents],
            ids=[doc.id for doc in documents],
        )
        self.logger.debug(f"Added {len(documents)} documents to the database")

    async def query(
        self,
        query_embedding: list[float],
        collection: str = DEFAULT_COLLECTION_NAME,
        k: int = 10,
    ) -> list[Document] | None:
        """Query the database for documents similar to the query embedding"""
        if not self.client:
            await self.init()

        try:
            collection = self.client.get_collection(name=collection)
        except Exception as e:
            self.logger.error(f"Error getting collection: {e}")
            return []

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
        )

        documents = []
        if results and results["documents"]:
            for i, content in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i]
                doc_id = results["ids"][0][i]
                documents.append(
                    Document(
                        id=doc_id,
                        title=metadata.get("title", "Unknown"),
                        content=content,
                        metadata=metadata,
                    )
                )

        self.logger.debug(f"Found {len(documents)} documents in the database")
        return documents

    async def get_documents(
        self, collection: str = DEFAULT_COLLECTION_NAME
    ) -> list[Document] | None:
        """List all documents in the database"""
        if not self.client:
            await self.init()

        try:
            collection = self.client.get_collection(name=collection)
        except Exception as e:
            self.logger.error(f"Error getting collection: {e}")
            return []

        response = collection.get()

        documents = []
        response_ids = response.get("ids")
        response_contents = response.get("documents")
        response_metadatas = response.get("metadatas")
        for doc_id, content, metadata in zip(
            response_ids, response_contents, response_metadatas, strict=False
        ):
            documents.append(
                Document(
                    id=doc_id,
                    title=metadata.get("title", "Unknown"),
                    content=content,
                    metadata=metadata,
                )
            )

        self.logger.debug(f"Found {len(documents)} documents in the database")
        return documents

    async def delete_all_documents(
        self, collection: str = DEFAULT_COLLECTION_NAME
    ) -> None:
        """Delete all documents in the database"""
        if not self.client:
            await self.init()

        self.client.delete_collection(name=collection)
        self.logger.debug("Deleted all documents in the database")
