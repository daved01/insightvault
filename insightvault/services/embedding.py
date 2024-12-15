from sentence_transformers import SentenceTransformer

from ..models.document import Document
from ..utils.logging import get_logger


class EmbeddingService:
    """Embedding service using sentence-transformers"""

    def __init__(self, model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model
        self.client = None
        self.logger = get_logger("insightvault.embedding")

    def init(self) -> None:
        """Initializes the embedding service with sentence-transformers model"""
        if self.client is None:
            self.client = SentenceTransformer(self.model_name)
        self.logger.debug(
            f"Initialized embedding service with model: {self.model_name}"
        )

    def embed(self, documents: list[Document]) -> list[Document]:
        """Embed a list of documents using sentence-transformers

        Args:
            documents: List of Document objects to embed

        Returns:
            List of Document objects with embeddings added
        """
        if self.client is None:
            self.init()
        self.logger.debug(f"Embedding {len(documents)} documents ...")
        # Extract text content from documents
        texts = [doc.content for doc in documents]

        # Generate embeddings
        embeddings = self.client.encode(
            texts, batch_size=32, show_progress_bar=False, convert_to_numpy=True
        )

        # Add embeddings back to documents
        for doc, embedding in zip(documents, embeddings, strict=False):
            doc.embedding = (
                embedding.tolist()
            )  # Convert numpy array to list for JSON serialization

        return documents
