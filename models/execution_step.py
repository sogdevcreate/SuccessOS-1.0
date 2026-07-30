from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ExecutionStep:
    """
    A single executable action.
    """

    handler: str
    action: str
    parameters: dict[str, Any]