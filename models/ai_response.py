"""
AI Response model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AIResponse:
    """
    Represents a response returned by an AI provider.
    """

    content: str

    provider: str

    model: str

    finish_reason: str = ""

    usage: dict[str, int] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)