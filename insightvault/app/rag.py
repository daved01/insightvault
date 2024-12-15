from ..models.document import Document
from .search import SearchApp


class RAGApp(SearchApp):
    """RAG application for retrieval-augmented generation

    This application extends the SearchApp with RAG-specific query functionality.
    All other methods (add_documents, delete_documents, etc.) are inherited from SearchApp.
    """

    def __init__(self, name: str = "insightvault.app.rag") -> None:
        super().__init__(name)

    # TODO: Implement this RAG-specific query functionality
    def query(self, query: str) -> list[Document]:
        """Query the database for documents similar to the query

        This RAG-specific implementation returns Document objects instead of strings.
        """
        self.logger.debug(f"RAG querying the database for: {query}")
        return super().get_event_loop().run_until_complete(self.async_query(query))

    # TODO: Implement this RAG-specific query functionality
    async def async_query(self, query: str) -> list[Document]:
        """Async version of query

        This RAG-specific implementation returns Document objects instead of strings.
        """
        self.logger.debug(f"RAG async querying the database for: {query}")
        response: list[Document] = await self.db.query(query)
        # TODO: Implement chat response
        return "This response is static, you have work to do."
