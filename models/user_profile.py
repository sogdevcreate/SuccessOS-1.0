"""
SuccessOS User Profile Model

Represents long-term information about the user.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class UserProfile:
    """
    Represents the user's long-term profile.
    """

    name: str = ""

    preferences: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)