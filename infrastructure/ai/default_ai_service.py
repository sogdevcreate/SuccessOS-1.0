"""
Default AI Service.

Default implementation of the AIService contract.
"""

from __future__ import annotations

from models.ai_request import AIRequest
from models.ai_response import AIResponse

from services.ai_provider import AIProvider
from services.ai_service import AIService


class DefaultAIService(AIService):
    """
    Default implementation of the AIService.

    Coordinates AI requests while remaining
    independent of any specific AI provider.
    """

    def __init__(
        self,
        provider: AIProvider,
    ) -> None:
        self._provider = provider

    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Generate an AI response using the configured provider.
        """

        return self._provider.generate(request)