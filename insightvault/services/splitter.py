from llama_index.core.node_parser import SentenceSplitter

from ..models.document import Document
from ..utils.logging import get_logger


class SplitterService:
    """Splitter service


    Attributes:
        chunk_size: The size of each chunk (default: 1024)
        chunk_overlap: The overlap between chunks (default: 256)
    """

    def __init__(self, chunk_size: int = 1024, chunk_overlap: int = 256):
        self.logger = get_logger("insightvault.splitter")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = SentenceSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

    def split(self, document: Document) -> list[Document]:
        """Split a document into chunks of a given size"""
        self.logger.debug(f"Splitting document: {document.title}")

        chunks = self.text_splitter.split_text(document.content)
        num_chunks = len(chunks)
        self.logger.debug(f"Number of chunks: {num_chunks}")
        split_documents = []
        for i, chunk in enumerate(chunks):
            split_documents.append(
                Document(
                    title=f"{document.title}",
                    content=chunk,
                    metadata={
                        **document.metadata,
                        "chunk_index": str(i),
                        "total_chunks": str(num_chunks),
                    },
                    embedding=document.embedding,
                    created_at=document.created_at,
                    updated_at=document.updated_at,
                )
            )

        return split_documents
