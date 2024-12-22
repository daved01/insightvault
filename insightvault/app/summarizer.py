import asyncio

from ..services.llm import OllamaLLMService
from ..services.prompt import PromptService
from .base import BaseApp


class SummarizerApp(BaseApp):
    """Summarizer application

    This application is used to summarize documents.
    """

    def __init__(self, name: str = "insightvault.app.summarizer") -> None:
        super().__init__(name)
        self.name = name
        self.prompt_service = PromptService()
        self.llm_service = OllamaLLMService()

    async def init(self) -> None:
        """Initialize the summarizer app"""
        # TODO: Use asyncio.gather() here, make it work with asyncio.run()
        # asyncio.gather(
        #     super().init(),
        #     self.llm_service.init(),
        # )
        await super().init()
        await self.llm_service.init()
        self.logger.debug(f"SummarizerApp `{self.name}` initialized!")

    def summarize(self, text: str) -> str | None:
        """Summarize a list of documents"""
        return asyncio.run(self.async_summarize(text=text))

    async def async_summarize(self, text: str) -> str | None:
        """Async version of summarize"""
        self.logger.info("Summarizing document(s) ...")

        prompt = self.prompt_service.get_prompt(
            prompt_type="summarize_text", context={"text": text}
        )

        response = await self.llm_service.query(prompt=prompt)
        return response
