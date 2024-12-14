from typing import List, Optional
from ..models.document import Document

class DatabaseService:
    def __init__(self, persist_directory: str = ".insightvault"):
        self.persist_directory = persist_directory
        
    async def init(self) -> None:
        """Initialize the database"""
        pass
        
    async def add_document(self, document: Document, collection: str = "default") -> None:
        """Add a document to the database"""
        pass
        
    async def query(
        self, 
        query: str, 
        collection: str = "default", 
        k: int = 5
    ) -> List[Document]:
        """Query the database"""
        pass