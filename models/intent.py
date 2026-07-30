"""
SuccessOS Intent Model

Represents the interpreted intent of a user's request.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from enums.intent_type import IntentType


@dataclass(slots=True)
class Intent:
    """
    Represents what the Intent Engine believes the user wants to do.
    """

    type: IntentType

    original_request: str

    confidence: float

    entities: dict[str, Any] = field(default_factory=dict)

    requires_clarification: bool = False

    clarification_question: str = ""