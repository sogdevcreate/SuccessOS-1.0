"""
SuccessOS Result Model

Defines the standard result returned by every operation in SuccessOS.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Result:
    """
    Represents the outcome of an operation.

    Every service, handler, and engine should return a Result
    instead of raising exceptions for expected failures.
    """

    success: bool
    message: str = ""
    data: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(
        cls,
        data: Any = None,
        message: str = "",
        **metadata: Any,
    ) -> "Result":
        """Create a successful result."""
        return cls(
            success=True,
            message=message,
            data=data,
            metadata=metadata,
        )

    @classmethod
    def fail(
        cls,
        message: str,
        error: str | None = None,
        **metadata: Any,
    ) -> "Result":
        """Create a failed result."""
        return cls(
            success=False,
            message=message,
            error=error,
            metadata=metadata,
        )

    def __bool__(self) -> bool:
        """Allow: if result:"""
        return self.success