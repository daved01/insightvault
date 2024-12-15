import chromadb
from chromadb.config import Settings

from ..constants import DEFAULT_COLLECTION_NAME
from ..models.document import Document
from ..utils.logging import get_logger


class DatabaseService:
    """Database service

    This service is used to interact with the database.
    """

    def __init__(
        self,
        persist_directory: str = "data/.db",
    ):
        self.persist_directory = persist_directory
        self.client = None
        self.logger = get_logger("insightvault.services.database")

    async def init(self) -> None:
        """Initialize the database"""

        # TODO: Factor this out into a provider
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )
        self.logger.debug("Database initialized")

    async def add_documents(
        self, documents: list[Document], collection: str = DEFAULT_COLLECTION_NAME
    ) -> None:
        """Add a list of documents to the database"""
        if not self.client:
            await self.init()

        # Get or create collection
        collection = self.client.get_or_create_collection(
            name=collection, metadata={"hnsw:space": "cosine"}
        )

        # Add the documents
        # TODO: Factor this out into a provider
        collection.add(
            documents=[doc.content for doc in documents],
            metadatas=[doc.metadata for doc in documents],
            embeddings=[doc.embedding for doc in documents],
            ids=[doc.id for doc in documents],
        )
        self.logger.debug(f"Added {len(documents)} documents to the database")

    async def query(
        self, query: str, collection: str = DEFAULT_COLLECTION_NAME, k: int = 5
    ) -> list[Document]:
        """Query the database"""
        if not self.client:
            await self.init()

        # Get collection
        collection = self.client.get_collection(
            name=collection, embedding_function=self.default_embedding_function
        )

        # Query the collection
        results = collection.query(query_texts=[query], n_results=k)

        # Convert results to Document objects
        documents = []
        if results and results["documents"]:
            for i, content in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i]
                doc_id = results["ids"][0][i]
                documents.append(
                    Document(id=doc_id, content=content, metadata=metadata)
                )

        self.logger.debug(f"Found {len(documents)} documents in the database")
        return documents

    async def get_documents(
        self, collection: str = DEFAULT_COLLECTION_NAME
    ) -> list[Document] | None:
        """List all documents in the database"""
        if not self.client:
            await self.init()

        # Get collection
        try:
            collection = self.client.get_collection(name=collection)
        except Exception as e:
            self.logger.error(f"Error getting collection: {e}")
            return []

        # List the documents
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
