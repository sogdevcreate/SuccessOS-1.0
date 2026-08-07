"""Trace entry for one action executed by an execution plan."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from enums.execution_status import ExecutionStatus
from enums.handler_type import HandlerType
from enums.operation_type import OperationType


@dataclass(slots=True)
class ExecutionTraceEntry:
    """Timing and outcome data for a single action."""

    action_name: str
    handler: HandlerType
    operation: OperationType
    started_at: datetime
    ended_at: datetime
    duration_seconds: float
    status: ExecutionStatus
    error: str = ""
