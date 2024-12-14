import asyncio
from .base import BaseApp
from ..services.database import DatabaseService
from ..models.document import Document
from ..services import ensure_list
from typing import Union, List

class RAGApp(BaseApp):
    """RAG application

    This application is used to query the database and add documents to the database.

    Attributes:
        db (Database): The database service.
    """
    def __init__(self, name: str = "insightvault") -> None:
        super().__init__(name)
        self.db = DatabaseService()

    @ensure_list(arg_name='query')
    def query(self, query: Union[str, List[str]]) -> list[Document]:
        """Query the database for documents similar to the query"""
        self.logger.info(f"Querying the database for: {query}")
        return asyncio.get_event_loop().run_until_complete(self.async_query(query))
    
    async def async_query(self, query: Union[str, List[str]]) -> list[Document]:
        """Async version of query"""
        self.logger.info(f"Async querying the database for: {query}")
        return await self.db.query(query)
    
    @ensure_list(arg_name='document')
    def add_documents(self, document: Union[Document, List[Document]]) -> None:
        """Add one or more documents to the database"""
        self.logger.info(f"Adding document(s)")
        return asyncio.get_event_loop().run_until_complete(self.async_add_document(document))
    
    @ensure_list(arg_name='document')
    async def async_add_documents(self, document: Union[Document, List[Document]]) -> None:
        """Async version of add_document"""
        self.logger.info(f"Async adding document(s)")
        return await self.db.add_document(document)
    
    @ensure_list(arg_name='document_id')
    def delete_documents(self, document_ids: Union[str, List[str]]) -> None:
        """Delete a document from the database"""
        self.logger.info(f"Deleting document(s)")
        return asyncio.get_event_loop().run_until_complete(self.async_delete_documents(document_ids))
    
    async def async_delete_documents(self, document_ids: Union[str, List[str]]) -> None:
        """Async version of delete_documents"""
        self.logger.info(f"Async deleting document(s)")
        return await self.db.delete_documents(document_ids)
    
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
