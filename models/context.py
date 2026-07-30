"""
SuccessOS Context Model

Represents all information available when interpreting
a user's request.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from models.memory_record import MemoryRecord
from models.system_status import SystemStatus
from models.user_profile import UserProfile


@dataclass(slots=True)
class Context:
    """
    Complete execution context supplied to the Intent Engine.
    """

    user_input: str

    conversation_history: list[str] = field(default_factory=list)

    memories: list[MemoryRecord] = field(default_factory=list)

    profile: UserProfile | None = None

    system_status: SystemStatus | None = None

    metadata: dict[str, Any] = field(default_factory=dict)