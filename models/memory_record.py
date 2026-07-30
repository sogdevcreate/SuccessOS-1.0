"""
SuccessOS Memory Record Model

Represents a single stored memory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from enums.memory_category import MemoryCategory


@dataclass(slots=True)
class MemoryRecord:
    """
    Represents a single memory stored by the Memory Service.
    """

    category: MemoryCategory

    key: str

    value: Any

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    metadata: dict[str, Any] = field(default_factory=dict)