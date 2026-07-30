"""
Router.
"""

from __future__ import annotations

from core.handler_registry import HandlerRegistry
from models.action import Action
from models.execution_result import ExecutionResult


class Router:
    """
    Routes actions to the appropriate handler.
    """

    def __init__(self, registry: HandlerRegistry) -> None:
        self._registry = registry

    def route(self, action: Action) -> ExecutionResult:
        """
        Route an action to its handler and execute it.
        """
        handler = self._registry.resolve(action.handler)
        return handler.execute(action)