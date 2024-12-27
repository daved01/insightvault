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
        self.llm_service = OllamaLLMService()

    async def init(self) -> None:
        """Initialize the RAG app"""
        # TODO: Use asyncio.gather() here, make it work with asyncio.run()
        # asyncio.gather(
        #     super().init(),
        #     self.llm_service.init(),
        # )
        await self.llm_service.init()
        await super().init()
        self.logger.debug(f"RAGApp `{self.name}` initialized!")

    def query(self, query: str) -> list[str]:
        """Query the database for documents similar to the query

        This RAG-specific implementation returns Document objects instead of strings.
        """
        return asyncio.run(self.async_query(query))

    async def async_query(self, query: str) -> list[str]:
        """Async version of query"""
        self.logger.debug(f"RAG async querying the database for: `{query}` ...")

        if not self.splitter_service:
            raise RuntimeError("Splitter service is not loaded!")
        if not self.embedder_service:
            raise RuntimeError("Embedding service is not loaded!")
        if not self.db_service:
            raise RuntimeError("Database service is not loaded!")

        query_embeddings: list[list[float]] = await self.embedder_service.embed([query])
        query_response: list[Document] | None = await self.db_service.query(
            query_embeddings[0]
        )

        # Create context from the response
        if not query_response:
            return ["No documents found in the database."]

        context = "\n".join([doc.content for doc in query_response])

        # Create prompt from the context
        prompt: str = self.prompt_service.get_prompt(
            prompt_type="rag_context", context={"question": query, "context": context}
        )

        response = await self.llm_service.query(prompt=prompt)
        if not response:
            return ["No response from the LLM."]
        return [response]

    def clear(self) -> None:
        """Clears the chat history"""
        return asyncio.run(self.async_clear())

    async def async_clear(self) -> None:
        """Async version of clear"""
        await self.llm_service.clear_chat_history()
