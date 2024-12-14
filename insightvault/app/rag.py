import asyncio
from .base import BaseApp
from ..services.database import DatabaseService
from ..models.document import Document

class RAGApp(BaseApp):
    """RAG application

    This application is used to query the database and add documents to the database.

    Attributes:
        db (Database): The database service.
    """
    def __init__(self, name: str = "insightvault") -> None:
        super().__init__(name)
        self.db = DatabaseService()

    def query(self, query: str) -> list[Document]:
        """Query the database for documents similar to the query"""
        self.logger.info(f"Querying the database for: {query}")
        return asyncio.get_event_loop().run_until_complete(self.async_query(query))
    
    async def async_query(self, query: str) -> list[Document]:
        """Async version of query"""
        self.logger.info(f"Async querying the database for: {query}")
        return await self.db.query(query)
    
    def add_document(self, document: Document) -> None:
        """Add a document to the database"""
        self.logger.info(f"Adding document: {document.id}")
        return asyncio.get_event_loop().run_until_complete(self.async_add_document(document))
    
    async def async_add_document(self, document: Document) -> None:
        """Async version of add_document"""
        self.logger.info(f"Async adding document: {document.id}")
        return await self.db.add_document(document)
    
    def delete_document(self, document_id: str) -> None:
        """Delete a document from the database"""
        self.logger.info(f"Deleting document: {document_id}")
        return asyncio.get_event_loop().run_until_complete(self.async_delete_document(document_id))
    
    async def async_delete_document(self, document_id: str) -> None:
        """Async version of delete_document"""
        self.logger.info(f"Async deleting document: {document_id}")
        return await self.db.delete_document(document_id)
    
    def delete_all_documents(self) -> None:
        """Delete all documents from the database"""
        self.logger.info("Deleting all documents ...")
        return asyncio.get_event_loop().run_until_complete(self.async_delete_all_documents())

    async def async_delete_all_documents(self) -> None:
        """Async version of delete_all_documents"""
        self.logger.info("Async deleting all documents ...")
        return await self.db.delete_all_documents()

    def list_documents(self) -> list[Document]:
        """List all documents in the database"""
        self.logger.info("Listing all documents ...")
        return asyncio.get_event_loop().run_until_complete(self.async_list_documents())

    async def async_list_documents(self) -> list[Document]:
        """Async version of list_documents"""
        self.logger.info("Async listing all documents ...")
        return await self.db.list_documents()
