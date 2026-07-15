from typing import Protocol


class AIProvider(Protocol):
    async def render_response(self, intent: str, message: str) -> str:
        """Render a conversational response without owning business rules."""


class MockAIProvider:
    async def render_response(self, intent: str, message: str) -> str:
        return message


class FutureOpenAIProvider:
    async def render_response(self, intent: str, message: str) -> str:
        raise NotImplementedError("External LLM providers are intentionally not implemented yet.")


class FutureGeminiProvider:
    async def render_response(self, intent: str, message: str) -> str:
        raise NotImplementedError("External LLM providers are intentionally not implemented yet.")
