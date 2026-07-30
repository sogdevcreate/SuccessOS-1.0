"""
Handler Type Enumeration

Identifies which handler is responsible for executing an action.
"""

from enum import Enum


class HandlerType(str, Enum):
    APPLICATION = "application"
    CHAT = "chat"
    SYSTEM = "system"
    MEMORY = "memory"
    NEWS = "news"
    INSTALLATION = "installation"
    FILESYSTEM = "filesystem"