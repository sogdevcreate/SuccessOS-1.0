"""
Handler interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from models.action import Action
from models.execution_result import ExecutionResult


class Handler(ABC):
    """
    Base contract for all handlers.
    """

    @abstractmethod
    def execute(self, action: Action) -> ExecutionResult:
        """
        Execute a single action.
        """
        raise NotImplementedError