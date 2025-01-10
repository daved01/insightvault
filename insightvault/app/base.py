import asyncio

import yaml

from ..models.config import AppConfig
from ..models.document import Document
from ..services.database import ChromaDatabaseService
from ..services.embedding import EmbeddingService
from ..services.splitter import SplitterService
from ..utils.logging import get_logger


class BaseApp:
    def __init__(
        self, name: str = "insightvault.app.base", config_path: str = "./config.yaml"
    ) -> None:
        self.name = name
        self.logger = get_logger(name)
        self.config = self._get_config(path=config_path)
        self.db_service = ChromaDatabaseService(config=self.config.database)
        self.splitter_service = SplitterService(config=self.config.splitter)
        self.embedder_service = EmbeddingService(config=self.config.embedding)

    async def init(self) -> None:
        """Initialize the app"""
        await self.embedder_service.init()
        self.logger.debug(f"BaseApp `{self.name}` initialized!")

    def add_documents(self, documents: list[Document]) -> None:
        """Add documents to the database"""
        self.logger.debug("Adding document(s)")
        return asyncio.run(self.async_add_documents(documents))

    async def async_add_documents(self, documents: list[Document]) -> None:
        """Async version of add_document"""
        self.logger.debug("Async adding document(s)")

        if not self.embedder_service:
            raise RuntimeError("Embedding service is not loaded!")

        processed_documents = []
        for doc in documents:
            # Split document into chunks
            chunks: list[Document] = self.splitter_service.split(doc)

            # Get embeddings for the chunk contents
            chunk_contents = [chunk.content for chunk in chunks]
            embeddings = await self.embedder_service.embed(chunk_contents)

            # Add embeddings to chunks
            for chunk, embedding in zip(chunks, embeddings, strict=True):
                chunk.embedding = embedding
                processed_documents.append(chunk)

        # Add processed documents to db
        return await self.db_service.add_documents(processed_documents)

    def delete_all_documents(self) -> None:
        """Delete all documents from the database"""
        self.logger.debug("Deleting all documents ...")
        return asyncio.run(self.async_delete_all_documents())

    async def async_delete_all_documents(self) -> None:
        """Async version of delete_all_documents"""
        self.logger.debug("Async deleting all documents ...")
        return await self.db_service.delete_all_documents()

    def list_documents(self) -> list[Document] | None:
        """List all documents in the database"""
        self.logger.debug("Listing all documents ...")
        return asyncio.run(self.async_list_documents())

    async def async_list_documents(self) -> list[Document] | None:
        """Async version of list_documents"""
        self.logger.debug("Async listing all documents ...")
        return await self.db_service.get_documents()

    def _get_config(self, path: str = "./config.yaml") -> AppConfig:
        """Reads the configuration file from the path"""
        with open(path) as file:
            config_data = yaml.safe_load(file)
        try:
            return AppConfig(**config_data)
        except Exception as e:
            print(f"Config validation error: {e}")
            raise
