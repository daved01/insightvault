import asyncio
from logging import Logger

from sentence_transformers import SentenceTransformer

from ..utils.logging import get_logger


class EmbeddingService:
    """Service for generating embeddings from text using sentence-transformers.

    To use it, you must first call `await get_client()` to ensure the model is loaded.


    Attributes:
        model_name: The name of the embedding model to use (default: "all-MiniLM-L6-v2")
        client: The embedding model client
        loading_task: The task that loads the embedding model
        logger: The logger for the embedding service
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.logger: Logger = get_logger("insightvault.services.embedding")
        self.model_name: str = model_name
        self.client: SentenceTransformer | None = None
        self.loading_task: asyncio.Task[None] = asyncio.create_task(self._load_model())

    async def _load_model(self) -> None:
        """Load the embedding model"""
        self.logger.debug(f"Loading embedding model: {self.model_name}")
        self.client = SentenceTransformer(self.model_name)
        self.logger.debug("Embedding model loaded!")

    async def get_client(self) -> SentenceTransformer:
        if self.client is None:
            self.logger.debug(
                "Embedding model not loaded, waiting for loading task to complete"
            )
            await self.loading_task

        # Better safe than sorry (and for mypy)
        if not self.client:
            raise RuntimeError("Client is not loaded!")
        return self.client

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (as lists of floats)
        """

        self.logger.debug(f"Embedding {len(texts)} texts...")
        if not self.client:
            self.client = await self.get_client()
        embeddings = self.client.encode(
            texts, batch_size=32, show_progress_bar=False, convert_to_numpy=True
        )

        # Convert numpy arrays to lists for JSON serialization
        return [embedding.tolist() for embedding in embeddings]
