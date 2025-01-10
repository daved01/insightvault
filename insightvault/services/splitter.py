from llama_index.core.node_parser import SentenceSplitter

from ..models.config import SplitterConfig
from ..models.document import Document
from ..utils.logging import get_logger


class SplitterService:
    """Splitter service


    Attributes:
        config: The configuration for the splitter
    """

    def __init__(self, config: SplitterConfig):
        self.logger = get_logger("insightvault.splitter")
        self.config = config
        self.text_splitter = SentenceSplitter(
            chunk_size=self.config.chunk_size, chunk_overlap=self.config.chunk_overlap
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
