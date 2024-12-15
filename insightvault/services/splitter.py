from ..models.document import Document
from ..utils.logging import get_logger


class SplitterService:
    """Splitter service"""

    def __init__(self, chunk_size: int = 256):
        self.chunk_size = chunk_size
        self.logger = get_logger("insightvault.splitter")

    def split(self, document: Document) -> list[Document]:
        """Split a document into chunks of a given size"""
        # TODO: Implement this
        self.logger.debug(f"Splitting document: {document.title}")
        return [document]
