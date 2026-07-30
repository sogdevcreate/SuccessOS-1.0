"""
AI Provider contract.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from models.ai_request import AIRequest
from models.ai_response import AIResponse


class AIProvider(ABC):
    """
    Base contract for all AI providers.
    """

    @abstractmethod
    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Generate a response from the AI provider.
        """
        raise NotImplementedError