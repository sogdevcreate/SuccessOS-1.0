"""
Context builder.
"""

from __future__ import annotations

from models.context import Context
from services.memory_service import MemoryService
from services.profile_service import ProfileService
from services.system_service import SystemService


class ContextBuilder:
    """
    Builds the execution context for the Intent Engine.
    """

    def __init__(
        self,
        memory_service: MemoryService,
        profile_service: ProfileService,
        system_service: SystemService,
    ) -> None:
        self._memory_service = memory_service
        self._profile_service = profile_service
        self._system_service = system_service

    def build(self, user_input: str) -> Context:
        """
        Build a context for the current request.
        """

        # TODO:
        # Replace list() with recall_all() after the MemoryService
        # interface is refactored to use domain-specific methods.

        return Context(
            user_input=user_input,
            memories=self._memory_service.list(),
            profile=self._profile_service.get_profile(),
            system_status=self._system_service.get_status(),
        )
