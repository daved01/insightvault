from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

import chromadb
from chromadb.config import Settings

from ..constants import (
    DEFAULT_COLLECTION_NAME,
)
from ..models.database import DistanceFunction
from ..models.document import Document
from ..utils.logging import get_logger


class AbstractDatabaseService(ABC):
    """Abstract database service"""

    @abstractmethod
    async def add_documents(self, documents: list[Document]) -> None:
        """Add a list of documents to the database"""

    @abstractmethod
    async def query(
        self,
        query_embedding: Sequence[float],
        collection_name: str = DEFAULT_COLLECTION_NAME,
        filter_docs: bool = True,
        k: int = 8,
    ) -> list[Document]:
        """Query the database for documents similar to the query embedding"""

    @abstractmethod
    async def get_documents(self) -> list[Document] | None:
        """Get all documents from the database"""

    @abstractmethod
    async def delete_all_documents(self) -> None:
        """Delete all documents from the database"""

    @abstractmethod
    def _get_db_value(self, distance: DistanceFunction) -> str:
        """Returns the database-specific string for the given distance function."""


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
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )
        self.similarity_function = self._get_db_value(DistanceFunction.COSINE)
        self.threshold = 0.9
        self.logger.debug("Database initialized")

    async def add_documents(
        self, documents: list[Document], collection_name: str = DEFAULT_COLLECTION_NAME
    ) -> None:
        """Add a list of documents to the database. The documents must have
        embeddings.
        """
        if not documents:
            self.logger.warning("No documents to add to the database")

        collection = self.client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": self.similarity_function}
        )

        collection.add(
            ids=[doc.id for doc in documents],
            documents=[doc.content for doc in documents],
            metadatas=[doc.metadata for doc in documents],
            embeddings=[doc.embedding for doc in documents],  # type: ignore
        )
        self.logger.debug(f"Added {len(documents)} documents to the database")

    async def query(
        self,
        query_embedding: Sequence[float],
        collection_name: str = DEFAULT_COLLECTION_NAME,
        filter_docs: bool = True,
        k: int = 8,
    ) -> list[Document]:
        """Query the database for documents similar to the query embedding"""

        try:
            collection = self.client.get_collection(name=collection_name)
        except Exception as e:
            self.logger.error(f"Error getting collection: {e}")
            return []

        results = collection.query(
            query_embeddings=[query_embedding],
            include=["documents", "metadatas", "distances"],  # type: ignore[list-item]
            n_results=k,
        )

        # Filter the documents based on the distance
        if filter_docs:
            self.logger.debug(f"Filtering documents with threshold: {self.threshold}")
            results = self._filter_docs(results=results, threshold=self.threshold)

        documents = []
        if results and results["documents"]:
            for i, content in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i]  # type: ignore
                doc_id = results["ids"][0][i]
                documents.append(
                    Document(
                        id=doc_id,
                        title=str(metadata.get("title", "Unknown")),
                        content=content,
                        metadata=metadata,
                    )
                )

        self.logger.debug(f"Found {len(documents)} documents in the database")
        return documents

    async def get_documents(
        self, collection_name: str = DEFAULT_COLLECTION_NAME
    ) -> list[Document] | None:
        """List all documents in the database"""

        try:
            collection = self.client.get_collection(name=collection_name)
        except Exception as e:
            self.logger.error(f"Error getting collection: {e}")
            return []

        response = collection.get()

        documents = []
        response_ids = response.get("ids")
        response_contents = response.get("documents")
        response_metadatas = response.get("metadatas")

        if response_ids and response_contents and response_metadatas:
            for doc_id, content, metadata in zip(
                response_ids, response_contents, response_metadatas, strict=False
            ):
                documents.append(
                    Document(
                        id=doc_id,
                        title=str(metadata.get("title", "Unknown")),
                        content=content,
                        metadata=metadata,
                    )
                )

        self.logger.debug(f"Found {len(documents)} documents in the database")
        return documents

    async def delete_all_documents(
        self, collection_name: str = DEFAULT_COLLECTION_NAME
    ) -> None:
        """Delete all documents in the database"""

        self.client.delete_collection(name=collection_name)
        self.logger.debug("Deleted all documents in the database")

    def _filter_docs(self, results: Any, threshold: float = 0.9) -> Any:
        """Filter the documents based on the distance"""
        ids_to_keep = []
        embeddings_to_keep = []
        documents_to_keep = []
        data_to_keep = []
        metadatas_to_keep = []

        # We don't need the distances after filtering
        for i in range(len(results["documents"][0])):
            if results["distances"][0][i] < threshold:
                continue
            documents_to_keep.append(results["documents"][0][i])
            embeddings_to_keep.append(results["embeddings"][0][i]) if results[
                "embeddings"
            ] else None
            metadatas_to_keep.append(results["metadatas"][0][i]) if results[
                "metadatas"
            ] else None
            ids_to_keep.append(results["ids"][0][i]) if results["ids"] else None
            data_to_keep.append(results["data"][0][i]) if results["data"] else None

        return {
            "ids": [ids_to_keep],
            "documents": [documents_to_keep],
            "metadatas": [metadatas_to_keep],
            "embeddings": [embeddings_to_keep],
            "data": [data_to_keep],
        }

    def _get_db_value(self, distance: DistanceFunction) -> str:
        if distance == DistanceFunction.COSINE:
            return "cosine"
        elif distance == DistanceFunction.L2:
            return "l2"
