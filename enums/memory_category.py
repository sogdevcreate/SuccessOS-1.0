"""
Memory Category Enumeration.
"""

from enum import Enum


class MemoryCategory(str, Enum):
    PROFILE = "profile"
    PREFERENCE = "preference"
    FACT = "fact"
    TASK = "task"
    CONVERSATION = "conversation"