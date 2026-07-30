"""
Application handler.
"""

from __future__ import annotations

from enums.operation_type import OperationType
from interfaces.handler import Handler
from models.action import Action
from models.execution_result import ExecutionResult
from services.application_service import ApplicationService


class ApplicationHandler(Handler):
    """
    Handles application-related actions.
    """

    def __init__(
        self,
        application_service: ApplicationService,
    ) -> None:
        self._application_service = application_service

    def execute(self, action: Action) -> ExecutionResult:
        """
        Execute an application action.
        """

        application = action.parameters.get("application")

        if not application:
            return ExecutionResult.fail(
                "Missing required parameter: 'application'."
            )

        match action.operation:

            case OperationType.OPEN:
                success = self._application_service.open(application)

            case OperationType.CLOSE:
                success = self._application_service.close(application)

            case _:
                return ExecutionResult.fail(
                    f"Unsupported operation: {action.operation.value}"
                )

        if not success:
            return ExecutionResult.fail(
                f"Failed to {action.operation.value} '{application}'."
            )

        return ExecutionResult.ok(
            message=(
                f"{action.operation.value.capitalize()}ed "
                f"'{application}' successfully."
            )
        )