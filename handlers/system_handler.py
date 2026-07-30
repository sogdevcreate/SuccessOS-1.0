"""
System handler.
"""

from __future__ import annotations

from enums.operation_type import OperationType
from interfaces.handler import Handler
from models.action import Action
from models.execution_result import ExecutionResult
from services.system_service import SystemService


class SystemHandler(Handler):
    """
    Handles system-related actions.
    """

    def __init__(
        self,
        system_service: SystemService,
    ) -> None:
        self._system_service = system_service

    def execute(self, action: Action) -> ExecutionResult:
        """
        Execute a system action.
        """

        match action.operation:

            case OperationType.QUERY:
                status = self._system_service.get_status()

                return ExecutionResult.ok(
                    message="System status retrieved successfully.",
                    payload=status,
                )

            case OperationType.SHUTDOWN:
                success = self._system_service.shutdown()

            case OperationType.RESTART:
                success = self._system_service.restart()

            case OperationType.SLEEP:
                success = self._system_service.sleep()

            case OperationType.LOCK:
                success = self._system_service.lock()

            case _:
                return ExecutionResult.fail(
                    f"Unsupported operation: {action.operation.value}"
                )

        if not success:
            return ExecutionResult.fail(
                f"Failed to execute '{action.operation.value}'."
            )

        return ExecutionResult.ok(
            message=f"'{action.operation.value}' executed successfully."
        )