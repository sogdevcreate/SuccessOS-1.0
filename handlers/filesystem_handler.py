"""
Filesystem handler.
"""

from __future__ import annotations

from pathlib import Path

from enums.operation_type import OperationType
from interfaces.handler import Handler
from models.action import Action
from models.execution_result import ExecutionResult
from services.filesystem_service import FilesystemService


class FilesystemHandler(Handler):
    """
    Handles filesystem actions.
    """

    def __init__(
        self,
        filesystem_service: FilesystemService,
    ) -> None:
        self._filesystem_service = filesystem_service

    def execute(
        self,
        action: Action,
    ) -> ExecutionResult:
        """
        Execute a filesystem action.
        """

        match action.operation:

            case OperationType.READ:

                path = action.parameters.get("path")

                if not isinstance(path, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'path'."
                    )

                file_path = Path(path)

                if not self._filesystem_service.exists(file_path):
                    return ExecutionResult.fail(
                        f"'{path}' does not exist."
                    )

                try:
                    content = self._filesystem_service.read_text(
                        file_path,
                    )

                    return ExecutionResult.ok(
                        message=content,
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.WRITE:

                path = action.parameters.get("path")
                content = action.parameters.get("content")

                if not isinstance(path, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'path'."
                    )

                if not isinstance(content, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'content'."
                    )

                try:
                    self._filesystem_service.write_text(
                        Path(path),
                        content,
                    )

                    return ExecutionResult.ok(
                        message="File written successfully."
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.LIST:

                path = action.parameters.get("path")

                if not isinstance(path, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'path'."
                    )

                try:
                    items = self._filesystem_service.list_directory(
                        Path(path),
                    )

                    return ExecutionResult.ok(
                        message="\n".join(
                            str(item)
                            for item in items
                        )
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.CREATE_DIRECTORY:

                path = action.parameters.get("path")

                if not isinstance(path, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'path'."
                    )

                try:
                    self._filesystem_service.create_directory(
                        Path(path),
                    )

                    return ExecutionResult.ok(
                        message="Directory created successfully."
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.DELETE:

                path = action.parameters.get("path")

                if not isinstance(path, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'path'."
                    )

                try:
                    self._filesystem_service.delete(
                        Path(path),
                    )

                    return ExecutionResult.ok(
                        message="Deleted successfully."
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.COPY:

                source = action.parameters.get("source")
                destination = action.parameters.get("destination")

                if not isinstance(source, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'source'."
                    )

                if not isinstance(destination, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'destination'."
                    )

                try:
                    self._filesystem_service.copy(
                        Path(source),
                        Path(destination),
                    )

                    return ExecutionResult.ok(
                        message="Copy completed successfully."
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.MOVE:

                source = action.parameters.get("source")
                destination = action.parameters.get("destination")

                if not isinstance(source, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'source'."
                    )

                if not isinstance(destination, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'destination'."
                    )

                try:
                    self._filesystem_service.move(
                        Path(source),
                        Path(destination),
                    )

                    return ExecutionResult.ok(
                        message="Move completed successfully."
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case OperationType.SEARCH:

                directory = action.parameters.get("directory")
                pattern = action.parameters.get("pattern")

                if not isinstance(directory, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'directory'."
                    )

                if not isinstance(pattern, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'pattern'."
                    )

                try:
                    results = self._filesystem_service.search(
                        Path(directory),
                        pattern,
                    )

                    return ExecutionResult.ok(
                        message="\n".join(
                            str(path)
                            for path in results
                        )
                    )

                except Exception as ex:
                    return ExecutionResult.fail(str(ex))

            case _:
                return ExecutionResult.fail(
                    f"Unsupported operation: {action.operation.value}"
                )