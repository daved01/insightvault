from typing import List, Optional
from ..models.document import Document
from ..constants import DEFAULT_COLLECTION_NAME
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# TODO: Make Chroma DB async
class DatabaseService:
    """Database service

    This service is used to interact with the database.
    """
    def __init__(self, persist_directory: str = "data/.db"):
        self.persist_directory = persist_directory
        self.client = None
        self.default_embedding_function = embedding_functions.DefaultEmbeddingFunction() # Gets `all-MiniLM-L6-v2`
    
    # TODO: This is not async right?
    async def init(self) -> None:
        """Initialize the database"""
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
      
    async def add_document(self, document: Document, collection: str = DEFAULT_COLLECTION_NAME) -> None:
        """Add a document to the database"""
        if not self.client:
            await self.init()
            
        # Get or create collection
        collection = self.client.get_or_create_collection(
            name=collection,
            embedding_function=self.default_embedding_function
        )
        
        # Add the document
        collection.add(
            documents=[document.content],
            metadatas=[document.metadata],
            ids=[document.id]
        )
        
    async def query(
        self, 
        query: str, 
        collection: str = DEFAULT_COLLECTION_NAME, 
        k: int = 5
    ) -> List[Document]:
        """Query the database"""
        if not self.client:
            await self.init()
            
        # Get collection
        collection = self.client.get_collection(
            name=collection,
            embedding_function=self.default_embedding_function
        )
        
        # Query the collection
        results = collection.query(
            query_texts=[query],
            n_results=k
        )
        
        # Convert results to Document objects
        documents = []
        if results and results['documents']:
            for i, content in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                doc_id = results['ids'][0][i]
                documents.append(Document(
                    id=doc_id,
                    content=content,
                    metadata=metadata
                ))
                
        return documents