"""
Permission Level Enumeration

Defines the level of user confirmation required before execution.
"""

from enum import Enum


class PermissionLevel(str, Enum):
    """Permission requirements."""

    NONE = "none"
    CONFIRM = "confirm"
    ADMIN = "admin"