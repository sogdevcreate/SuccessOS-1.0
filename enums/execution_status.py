"""
Execution Status Enumeration

Represents the lifecycle state of an operation.
"""

from enum import Enum


class ExecutionStatus(str, Enum):
    """Possible execution states."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"