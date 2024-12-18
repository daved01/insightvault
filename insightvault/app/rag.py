import asyncio

from ..models.document import Document
from ..services.llm import OllamaLLMService
from ..services.prompt import PromptService
from .search import SearchApp


class RAGApp(SearchApp):
    """RAG application for retrieval-augmented generation

    This application extends the SearchApp with RAG-specific query functionality.
    All other methods (add_documents, delete_documents, etc.) are inherited from SearchApp.
    """

    def __init__(self, name: str = "insightvault.app.rag") -> None:
        super().__init__(name)
        self.prompt_service = PromptService()
        self.llm = OllamaLLMService()

    def query(self, query: str) -> list[Document]:
        """Query the database for documents similar to the query

        This RAG-specific implementation returns Document objects instead of strings.
        """
        self.logger.debug(f"RAG querying the database for: {query}")
        return asyncio.get_event_loop().run_until_complete(self.async_query(query))

    # TODO: Implement this RAG-specific query functionality
    async def async_query(self, query: str) -> list[Document]:
        """Async version of query

        This RAG-specific implementation returns Document objects instead of strings.
        """
        self.logger.debug(f"RAG async querying the database for: {query}")
        query_embeddings: list[list[float]] = self.embedder.embed([query])
        response: list[Document] = await self.db.query(query_embeddings[0])

        # Create context from the response
        context = "\n".join([doc.content for doc in response])

        # Create prompt from the context
        prompt = self.prompt_service.get_prompt(
            prompt_type="rag_context", context={"question": query, "context": context}
        )

        # Query the LLM
        response = await self.llm.query(prompt=prompt)
        return response
