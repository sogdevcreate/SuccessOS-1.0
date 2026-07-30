"""
Intent Type Enumeration

Represents the high-level intent extracted from a user request.
"""

from enum import Enum


class IntentType(str, Enum):
    """Supported intent categories."""

    CHAT = "chat"
    APPLICATION = "application"
    SYSTEM = "system"
    MEMORY = "memory"
    NEWS = "news"
    INSTALLATION = "installation"
    TASK = "task"
    UNKNOWN = "unknown"