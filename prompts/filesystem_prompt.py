"""Filesystem action definitions for the planner prompt."""

from textwrap import dedent


FILESYSTEM_PROMPT = dedent(
    """
    ==================================================
    FILESYSTEM
    ==================================================

    Operations:
    - READ
    - WRITE
    - LIST
    - COPY
    - MOVE
    - DELETE
    - SEARCH
    - CREATE_DIRECTORY

    READ
    {"path": "<file path>"}

    WRITE
    {"path": "<file path>", "content": "<text>"}

    LIST
    {"path": "<directory path>"}

    DELETE
    {"path": "<file or directory path>"}

    COPY
    {"source": "<source path>", "destination": "<destination path>"}

    MOVE
    {"source": "<source path>", "destination": "<destination path>"}

    SEARCH
    {"directory": "<directory path>", "pattern": "<search pattern>"}

    CREATE_DIRECTORY
    {"path": "<directory path>"}
    """
).strip()
