"""Memory action definitions for the planner prompt."""

from textwrap import dedent


MEMORY_PROMPT = dedent(
    """
    ==================================================
    MEMORY
    ==================================================

    Operations:
    - SAVE
    - LOAD
    - DELETE

    Valid categories:
    - profile
    - preference
    - fact
    - task
    - conversation

    SAVE
    {"category": "<profile|preference|fact|task|conversation>", "key": "<key>", "value": "<value>"}

    LOAD
    {"category": "<profile|preference|fact|task|conversation>", "key": "<key>"}

    DELETE
    {"category": "<profile|preference|fact|task|conversation>", "key": "<key>"}
    """
).strip()
