import chromadb
from chromadb.config import Settings

from ..constants import DEFAULT_COLLECTION_NAME
from ..models.document import Document


class DatabaseService:
    """Database service

    This service is used to interact with the database.
    """

    def __init__(self, persist_directory: str = "data/.db"):
        self.persist_directory = persist_directory
        self.client = None

    async def init(self) -> None:
        """Initialize the database"""

        # TODO: Factor this out into a provider
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )

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

        return documents
