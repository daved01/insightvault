import asyncio
from logging import Logger

from sentence_transformers import SentenceTransformer

from ..models.config import EmbeddingConfig
from ..utils.logging import get_logger


class EmbeddingService:
    """Service for generating embeddings from text using sentence-transformers.

    To use it, you must first call `await get_client()` to ensure the model is loaded.


    Attributes:
        config: The configuration for the embedding service
        client: The embedding model client
        loading_task: The task that loads the embedding model
        logger: The logger for the embedding service
    """

    def __init__(self, config: EmbeddingConfig) -> None:
        self.logger: Logger = get_logger("insightvault.services.embedding")
        self.config = config
        self.client: SentenceTransformer | None = None

    async def init(self) -> None:
        """Initialize the embedding service"""
        self.client = await asyncio.to_thread(SentenceTransformer, self.config.model)
        self.logger.debug(f"Embedding model loaded `{self.config.model}`!")

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (as lists of floats)
        """

        self.logger.debug(f"Embedding {len(texts)} texts...")

        if not self.client:
            raise RuntimeError("Embedding model is not loaded! Call `init()` first.")

        embeddings = self.client.encode(
            texts, batch_size=32, show_progress_bar=False, convert_to_numpy=True
        )

        # Convert numpy arrays to lists for JSON serialization
        return [embedding.tolist() for embedding in embeddings]
