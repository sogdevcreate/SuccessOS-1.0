"""
Installation handler.
"""

from __future__ import annotations

from enums.operation_type import OperationType
from interfaces.handler import Handler
from models.action import Action
from models.execution_result import ExecutionResult
from services.installation_service import InstallationService


class InstallationHandler(Handler):
    """
    Handles software installation actions.
    """

    def __init__(
        self,
        installation_service: InstallationService,
    ) -> None:
        self._installation_service = installation_service

    def execute(self, action: Action) -> ExecutionResult:
        """
        Execute an installation action.
        """

        application = action.parameters.get("application")

        if not application:
            return ExecutionResult.fail(
                "Missing required parameter: 'application'."
            )

        match action.operation:

            case OperationType.INSTALL:
                success = self._installation_service.install(application)

            case OperationType.UNINSTALL:
                success = self._installation_service.uninstall(application)

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