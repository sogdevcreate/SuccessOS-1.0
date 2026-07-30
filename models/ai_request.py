"""
AI Request model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AIRequest:
    """
    Represents a request sent to an AI provider.
    """

    prompt: str

    system_prompt: str = ""

    temperature: float = 0.7

    max_tokens: int = 1024

    metadata: dict[str, Any] = field(default_factory=dict)