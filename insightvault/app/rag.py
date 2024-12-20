import asyncio

from ..models.document import Document
from ..services.llm import OllamaLLMService
from ..services.prompt import PromptService
from .search import SearchApp


class RAGApp(SearchApp):
    """RAG application for retrieval-augmented generation

    This application extends the SearchApp with RAG-specific query functionality.
    All other methods (add_documents, delete_documents, etc.) are inherited from
    SearchApp.
    """

    def __init__(self, name: str = "insightvault.app.rag") -> None:
        super().__init__(name)
        self.prompt_service = PromptService()
        self.llm: OllamaLLMService | None = None

    async def _init_rag(self) -> None:
        """Initialize the RAG part of the application"""
        self.logger.debug("Initializing RAG application")
        self.llm = OllamaLLMService()
        if not self.llm:
            raise RuntimeError("LLM service is not loaded!")
        await self.llm.get_client()
        self.logger.debug("RAG application initialized")

    async def init_rag(self) -> None:
        """Initialize the RAG application"""
        # TODO: This should be done with asyncio.gather
        await self.init_base()
        await self._init_rag()

    def query(self, query: str) -> list[str]:
        """Query the database for documents similar to the query

        This RAG-specific implementation returns Document objects instead of strings.
        """
        self.logger.debug(f"RAG querying the database for: {query}")
        return asyncio.get_event_loop().run_until_complete(self.async_query(query))

    async def async_query(self, query: str) -> list[str]:
        """Async version of query

        This RAG-specific implementation returns Document objects instead of strings.
        """
        self.logger.debug(f"RAG async querying the database for: {query}")
        await self.init_rag()
        if not self.embedder:
            raise RuntimeError("Embedding service is not loaded!")
        if not self.db:
            raise RuntimeError("Database service is not loaded!")
        query_embeddings: list[list[float]] = await self.embedder.embed([query])
        query_response: list[Document] | None = await self.db.query(query_embeddings[0])

        # Create context from the response
        if not query_response:
            return ["No documents found in the database."]

        context = "\n".join([doc.content for doc in query_response])

        # Create prompt from the context
        prompt: str = self.prompt_service.get_prompt(
            prompt_type="rag_context", context={"question": query, "context": context}
        )

        # Query the LLM
        if not self.llm:
            raise RuntimeError("LLM service is not loaded!")
        response = await self.llm.query(prompt=prompt)
        if not response:
            return ["No response from the LLM."]
        return [response]
