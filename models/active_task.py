"""
SuccessOS Active Task Model

Represents a task currently being executed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from enums.execution_status import ExecutionStatus


@dataclass(slots=True)
class ActiveTask:
    """
    Represents an active execution task.
    """

    task_id: str

    description: str

    status: ExecutionStatus = ExecutionStatus.PENDING

    progress: float = 0.0

    created_at: datetime = field(default_factory=datetime.utcnow)

    started_at: datetime | None = None

    completed_at: datetime | None = None