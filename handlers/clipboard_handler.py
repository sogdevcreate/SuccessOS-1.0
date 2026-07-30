"""
Clipboard handler.
"""

from __future__ import annotations

from enums.operation_type import OperationType
from interfaces.handler import Handler
from models.action import Action
from models.execution_result import ExecutionResult
from services.clipboard_service import ClipboardService


class ClipboardHandler(Handler):
    """
    Handles clipboard actions.
    """

    def __init__(
        self,
        clipboard_service: ClipboardService,
    ) -> None:
        self._clipboard_service = clipboard_service

    def execute(
        self,
        action: Action,
    ) -> ExecutionResult:
        """
        Execute a clipboard action.
        """

        match action.operation:

            case OperationType.COPY:

                text = action.parameters.get("text")

                if not isinstance(text, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'text'."
                    )

                try:
                    self._clipboard_service.set_text(text)

                    return ExecutionResult.ok(
                        message="Clipboard updated successfully."
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.READ:

                try:
                    text = self._clipboard_service.get_text()

                    return ExecutionResult.ok(
                        message=text,
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.CLEAR:

                try:
                    self._clipboard_service.clear()

                    return ExecutionResult.ok(
                        message="Clipboard cleared."
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case _:

                return ExecutionResult.fail(
                    f"Unsupported operation: {action.operation.value}"
                )