"""Generic browser action definitions for the planner prompt."""

from textwrap import dedent


BROWSER_PROMPT = dedent(
    """
    ==================================================
    BROWSER
    ==================================================

    Command intent mapping:
    - "Open https://..." means OPEN_URL.
    - "Open new tab https://..." means OPEN_TAB.
    - "Click <element>" means CLICK.
    - "Type <text> into <element>" means TYPE, even when <text> begins with "Open".
    - "Press <key>" means PRESS.
    - "Scroll down" means SCROLL.
    - "Select <option>" means SELECT.
    - "Upload file <path>" means UPLOAD_FILE.

    Operations:
    - OPEN_URL
    - OPEN_TAB
    - CLOSE_TAB
    - REFRESH_PAGE
    - GO_BACK
    - GO_FORWARD
    - LIST_TABS
    - CURRENT_TAB
    - SWITCH_TAB
    - PAGE_TITLE
    - CLICK
    - TYPE
    - PRESS
    - WAIT_FOR
    - SCROLL
    - SELECT
    - UPLOAD_FILE
    - SCREENSHOT

    OPEN_URL or OPEN_TAB
    {"url": "<url>"}

    SWITCH_TAB
    {"index": <tab number starting from 1>}

    CLICK
    {"selector": "<element name or selector>"}

    TYPE
    {"selector": "<element name or selector>", "text": "<text>"}

    PRESS
    {"key": "<ENTER|TAB|ESCAPE|SPACE|BACKSPACE|DELETE|UP|DOWN|LEFT|RIGHT>"}

    WAIT_FOR
    {"selector": "<element name or selector>", "timeout": 10}

    SCROLL
    {"pixels": 500}

    SELECT
    {"selector": "<element name or selector>", "value": "<visible option text>"}

    UPLOAD_FILE
    {"selector": "<element name or selector>", "path": "<file path>"}

    SCREENSHOT
    {"path": "<output file>"}

    CLOSE_TAB, REFRESH_PAGE, GO_BACK, GO_FORWARD, LIST_TABS, CURRENT_TAB, and PAGE_TITLE use {}.
    """
).strip()
