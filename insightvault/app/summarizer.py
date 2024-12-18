import asyncio

from ..services.llm import OllamaLLMService
from ..services.prompt import PromptService
from .base import BaseApp


class SummarizerApp(BaseApp):
    """Summarizer application

    This application is used to summarize documents.
    """

    def __init__(self, name: str = "insightvault") -> None:
        super().__init__(name)
        self.llm = OllamaLLMService()
        self.prompt_service = PromptService()

    def summarize(self, text: str) -> str:
        """Summarize a list of documents"""
        self.logger.info("Summarizing document(s)")
        return asyncio.get_event_loop().run_until_complete(
            self.async_summarize(text=text)
        )

    async def async_summarize(self, text: str) -> str:
        """Async version of summarize"""
        self.logger.info("Async summarizing document(s)")

        prompt = self.prompt_service.get_prompt(
            prompt_type="summarize_text", context={"text": text}
        )

        response = await self.llm.query(prompt=prompt)
        return response
