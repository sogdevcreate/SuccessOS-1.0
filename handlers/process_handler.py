"""
Process handler.
"""

from __future__ import annotations

from enums.operation_type import OperationType
from interfaces.handler import Handler
from models.action import Action
from models.execution_result import ExecutionResult
from services.process_service import ProcessService


class ProcessHandler(Handler):
    """
    Handles process management actions.
    """

    def __init__(
        self,
        process_service: ProcessService,
    ) -> None:
        self._process_service = process_service

    def execute(
        self,
        action: Action,
    ) -> ExecutionResult:
        """
        Execute a process management action.
        """

        match action.operation:

            case OperationType.LIST_PROCESSES:

                try:
                    processes = self._process_service.list_processes()

                    lines = [
                        (
                            f"{process['pid']:>6}  "
                            f"{process['name']}"
                        )
                        for process in processes
                    ]

                    return ExecutionResult.ok(
                        message="\n".join(lines),
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.START_PROCESS:

                command = action.parameters.get("command")

                if not isinstance(command, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'command'."
                    )

                try:
                    self._process_service.start_process(
                        command,
                    )

                    return ExecutionResult.ok(
                        message="Process started successfully.",
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.KILL_PROCESS:

                process = action.parameters.get("process")

                if not isinstance(process, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'process'."
                    )

                try:
                    self._process_service.kill_process(
                        process,
                    )

                    return ExecutionResult.ok(
                        message="Process terminated successfully.",
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.PROCESS_INFO:

                process = action.parameters.get("process")

                if not isinstance(process, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'process'."
                    )

                try:
                    info = self._process_service.process_info(
                        process,
                    )

                    return ExecutionResult.ok(
                        message=(
                            f"PID: {info['pid']}\n"
                            f"Name: {info['name']}\n"
                            f"Status: {info['status']}\n"
                            f"Memory: {info['memory']}\n"
                            f"CPU: {info['cpu']}%"
                        ),
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case _:

                return ExecutionResult.fail(
                    f"Unsupported operation: {action.operation.value}"
                )