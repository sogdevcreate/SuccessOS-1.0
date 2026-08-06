"""Planner rules shared by all prompt components."""

from textwrap import dedent


RULES_PROMPT = dedent(
    """
    ==================================================
    RULES
    ==================================================

    - Never invent handlers, operations, parameter names, or memory categories.
    - Use "preference", never "preferences".
    - Return ONLY valid JSON.
    - "YouTube Studio" is a browser feature, not an application.
    - If the user says "Open YouTube Studio" or "Open Studio", use STUDIO_OPEN.
    - Never use APPLICATION OPEN for YouTube Studio.
    - Never use OPEN_URL for YouTube Studio unless the user explicitly provides a URL.

    Handler names must exactly match:
    APPLICATION
    INSTALLATION
    MEMORY
    FILESYSTEM
    CLIPBOARD
    PROCESS
    BROWSER
    NEWS
    SYSTEM
    """
).strip()
