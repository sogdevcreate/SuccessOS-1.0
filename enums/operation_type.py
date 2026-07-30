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

    # Clipboard
    CLEAR = "clear"

    # Process
    LIST_PROCESSES = "list_processes"
    START_PROCESS = "start_process"
    KILL_PROCESS = "kill_process"
    PROCESS_INFO = "process_info"

    # System
    SHUTDOWN = "shutdown"
    RESTART = "restart"
    SLEEP = "sleep"
    LOCK = "lock"

    # Chat
    CHAT = "chat"