"""
Central authorization policy for executable actions.
"""

from __future__ import annotations

import ctypes
import os
from collections.abc import Callable

from enums.handler_type import HandlerType
from enums.operation_type import OperationType
from enums.permission_level import PermissionLevel
from models.action import Action
from models.execution_result import ExecutionResult


ConfirmationProvider = Callable[[Action, PermissionLevel], bool]
AdminChecker = Callable[[], bool]


class PermissionManager:
    """Determine and enforce the authorization needed for an action."""

    _CONFIRMATION_REQUIRED = frozenset({
        (HandlerType.FILESYSTEM, OperationType.DELETE),
        (HandlerType.FILESYSTEM, OperationType.MOVE),
        (HandlerType.INSTALLATION, OperationType.INSTALL),
        (HandlerType.INSTALLATION, OperationType.UNINSTALL),
        (HandlerType.PROCESS, OperationType.KILL_PROCESS),
        (HandlerType.PROCESS, OperationType.START_PROCESS),
        (HandlerType.BROWSER, OperationType.UPLOAD_FILE),
        (HandlerType.SYSTEM, OperationType.SHUTDOWN),
        (HandlerType.SYSTEM, OperationType.RESTART),
    })

    def __init__(
        self,
        confirmation_provider: ConfirmationProvider | None = None,
        admin_checker: AdminChecker | None = None,
    ) -> None:
        self._confirmation_provider = (
            confirmation_provider or self._request_confirmation
        )
        self._admin_checker = admin_checker or self._is_administrator

    def required_level(self, action: Action) -> PermissionLevel:
        """Return the effective permission level for an action."""

        if action.permission == PermissionLevel.ADMIN:
            return PermissionLevel.ADMIN

        if (
            action.permission == PermissionLevel.CONFIRM
            or action.requires_confirmation
            or (action.handler, action.operation)
            in self._CONFIRMATION_REQUIRED
        ):
            return PermissionLevel.CONFIRM

        return PermissionLevel.NONE

    def authorize(self, action: Action) -> ExecutionResult | None:
        """Authorize an action, returning a failure result when it is denied."""

        level = self.required_level(action)

        if level == PermissionLevel.NONE:
            return None

        if level == PermissionLevel.ADMIN and not self._admin_checker():
            return ExecutionResult.fail(
                "Action requires administrator privileges.",
                metadata={"permission": level.value},
            )

        if not self._confirmation_provider(action, level):
            return ExecutionResult.fail(
                "Action was not authorized by the user.",
                metadata={"permission": level.value},
            )

        return None

    @staticmethod
    def _request_confirmation(
        action: Action,
        level: PermissionLevel,
    ) -> bool:
        """Prompt interactively for an authorization decision."""

        prompt = (
            f"Allow {action.handler.value}/{action.operation.value} "
            f"({level.value})? [y/N]: "
        )

        try:
            return input(prompt).strip().lower() in {"y", "yes"}
        except EOFError:
            return False

    @staticmethod
    def _is_administrator() -> bool:
        """Return whether the current Windows process is elevated."""

        if os.name != "nt":
            return False

        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except (AttributeError, OSError):
            return False
