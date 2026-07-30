"""
AI Service contract.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from models.ai_request import AIRequest
from models.ai_response import AIResponse


class AIService(ABC):
    """
    High-level AI service.

    Coordinates AI interactions while remaining
    independent of any specific provider.
    """

    @abstractmethod
    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Generate an AI response.
        """
        raise NotImplementedError