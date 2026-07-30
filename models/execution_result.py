"""
SuccessOS Execution Result Model

Represents the outcome of executing an ExecutionPlan.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from enums.execution_status import ExecutionStatus


@dataclass(slots=True)
class ExecutionResult:
    """
    Represents the result of executing one or more actions.
    """

    status: ExecutionStatus

    message: str = ""

    payload: Any = None

    completed_actions: int = 0

    total_actions: int = 0

    errors: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def successful(self) -> bool:
        """
        True when execution completed successfully.
        """
        return self.status == ExecutionStatus.SUCCESS

    @classmethod
    def ok(
        cls,
        message: str = "",
        payload: Any = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ExecutionResult":
        """
        Create a successful execution result.
        """
        return cls(
            status=ExecutionStatus.SUCCESS,
            message=message,
            payload=payload,
            metadata=metadata or {},
        )

    @classmethod
    def fail(
        cls,
        message: str,
        errors: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ExecutionResult":
        """
        Create a failed execution result.
        """
        return cls(
            status=ExecutionStatus.FAILED,
            message=message,
            errors=errors or [],
            metadata=metadata or {},
        )