"""
Handler registry.
"""

from __future__ import annotations

from interfaces.handler import Handler
from enums.handler_type import HandlerType


class HandlerRegistry:
    """
    Maps handler types to handler instances.
    """

    def __init__(self) -> None:
        self._handlers: dict[HandlerType, Handler] = {}

    def register(
        self,
        handler_type: HandlerType,
        handler: Handler,
    ) -> None:
        """
        Register a handler.
        """
        self._handlers[handler_type] = handler

    def resolve(
        self,
        handler_type: HandlerType,
    ) -> Handler:
        """
        Return the registered handler.
        """
        try:
            return self._handlers[handler_type]
        except KeyError as exc:
            raise ValueError(
                f"No handler registered for '{handler_type.value}'."
            ) from exc