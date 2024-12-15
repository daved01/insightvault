from sentence_transformers import SentenceTransformer

from ..utils.logging import get_logger


class EmbeddingService:
    """Service for generating embeddings from text using sentence-transformers"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.logger = get_logger("insightvault.services.embedding")
        self.model_name = model_name
        self.client = None

    def init(self) -> None:
        """Initialize the embedding model"""
        self.client = SentenceTransformer(self.model_name)
        self.logger.debug(f"Initialized embedding model: {self.model_name}")

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (as lists of floats)
        """
        if self.client is None:
            self.init()

        self.logger.debug(f"Embedding {len(texts)} texts...")
        embeddings = self.client.encode(
            texts, batch_size=32, show_progress_bar=False, convert_to_numpy=True
        )

        # Convert numpy arrays to lists for JSON serialization
        return [embedding.tolist() for embedding in embeddings]
