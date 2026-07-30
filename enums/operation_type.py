"""
Operation Type Enumeration.

Represents the operation an Action requests.
"""

from enum import Enum


class OperationType(str, Enum):
    # Application
    OPEN = "open"
    CLOSE = "close"

    # Installation
    INSTALL = "install"
    UNINSTALL = "uninstall"

    # AI / Search
    QUERY = "query"
    SEARCH = "search"

    # Memory
    SAVE = "save"
    LOAD = "load"
    DELETE = "delete"

    # Filesystem
    READ = "read"
    WRITE = "write"
    LIST = "list"
    COPY = "copy"
    MOVE = "move"
    CREATE_DIRECTORY = "create_directory"

    # System
    SHUTDOWN = "shutdown"
    RESTART = "restart"
    SLEEP = "sleep"
    LOCK = "lock"

    # Chat
    CHAT = "chat"