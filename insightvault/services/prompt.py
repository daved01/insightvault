class PromptService:
    """Prompt service"""

    def __init__(self) -> None:
        """Initialize the prompt service"""
        self.prompts: dict[str, str] = {
            "summarize_text": (
                "Summarize the text below after the colon at the end. "
                "Only use this text. "
                "Do not add any information that is not part of the text. "
                "Make the summary concise. Mirror the style of the input text. "
                "Text to summarize: {text}"
            ),
            "rag_context": (
                "You are a friendly, helpful assistant. "
                "You are given a question and some context below. "
                "Use the context to answer the question. "
                "Do not make up information, only use the information in the context. "
                "If context below does not contain the answer, that is fine. Do not "
                "use information other that what is in the context."
                "If you don't know the answer, say 'I don't know'. "
                "Question: {question}\n"
                "Context: {context}"
            ),
        }

    def get_prompt(
        self, prompt_type: str, context: dict[str, str] | None = None
    ) -> str:
        """
        Retrieves a predefined prompt for a specific use case and injects
        context if needed. The context can include parameters like 'text', etc.

        Args:
            prompt_type (str): The type of prompt to retrieve.
            context (dict | None): The context to inject into the prompt.

        Returns:
            str: The prompt with the injected context.
        """
        base_prompt = self.prompts.get(prompt_type)
        if not base_prompt:
            raise ValueError(f"Prompt for key '{prompt_type}' not found.")

        if context:
            return base_prompt.format(**context)

        return base_prompt
