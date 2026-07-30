"""
Memory handler.
"""

from __future__ import annotations

from enums.memory_category import MemoryCategory
from enums.operation_type import OperationType
from interfaces.handler import Handler
from models.action import Action
from models.execution_result import ExecutionResult
from models.memory_record import MemoryRecord
from services.memory_service import MemoryService


class MemoryHandler(Handler):
    """
    Handles memory-related actions.
    """

    def __init__(
        self,
        memory_service: MemoryService,
    ) -> None:
        self._memory_service = memory_service

    def execute(self, action: Action) -> ExecutionResult:
        """
        Execute a memory action.
        """

        match action.operation:

            case OperationType.SAVE:

                category = action.parameters.get("category")
                key = action.parameters.get("key")
                value = action.parameters.get("value")

                if not isinstance(category, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'category'."
                    )

                if not isinstance(key, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'key'."
                    )

                if value is None:
                    return ExecutionResult.fail(
                        "Missing required parameter: 'value'."
                    )

                try:
                    category_enum = MemoryCategory[
                        category.upper()
                    ]
                except KeyError:
                    return ExecutionResult.fail(
                        f"Invalid memory category: '{category}'."
                    )

                memory = MemoryRecord(
                    category=category_enum,
                    key=key,
                    value=value,
                )

                success = self._memory_service.remember(memory)

                if not success:
                    return ExecutionResult.fail(
                        "Failed to store memory."
                    )

                return ExecutionResult.ok(
                    message="Memory stored successfully."
                )

            case OperationType.LOAD:

                category = action.parameters.get("category")
                key = action.parameters.get("key")

                if not isinstance(category, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'category'."
                    )

                if not isinstance(key, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'key'."
                    )

                try:
                    category_enum = MemoryCategory[
                        category.upper()
                    ]
                except KeyError:
                    return ExecutionResult.fail(
                        f"Invalid memory category: '{category}'."
                    )

                memory = self._memory_service.recall(
                    category_enum,
                    key,
                )

                if memory is None:
                    return ExecutionResult.ok(
                        message=f"I don't have a memory for '{key}'."
                    )

                return ExecutionResult.ok(
                    message=f"{memory.value}"
                )

            case OperationType.DELETE:

                category = action.parameters.get("category")
                key = action.parameters.get("key")

                if not isinstance(category, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'category'."
                    )

                if not isinstance(key, str):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'key'."
                    )

                try:
                    category_enum = MemoryCategory[
                        category.upper()
                    ]
                except KeyError:
                    return ExecutionResult.fail(
                        f"Invalid memory category: '{category}'."
                    )

                success = self._memory_service.forget(
                    category_enum,
                    key,
                )

                if not success:
                    return ExecutionResult.fail(
                        "Failed to remove memory."
                    )

                return ExecutionResult.ok(
                    message="Memory removed successfully."
                )

            case _:
                return ExecutionResult.fail(
                    f"Unsupported operation: {action.operation.value}"
                )