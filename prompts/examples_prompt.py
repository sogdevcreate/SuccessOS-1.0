"""Few-shot examples for planner output."""

from textwrap import dedent


EXAMPLES_PROMPT = dedent(
    """
    ==================================================
    EXAMPLES
    ==================================================

    User: Open https://www.youtube.com
    {"actions": [{"handler": "BROWSER", "operation": "OPEN_URL", "parameters": {"url": "https://www.youtube.com"}}]}

    User: Open example.com in a new tab
    {"actions": [{"handler": "BROWSER", "operation": "OPEN_TAB", "parameters": {"url": "https://example.com"}}]}

    User: Click the Sign in button
    {"actions": [{"handler": "BROWSER", "operation": "CLICK", "parameters": {"selector": "Sign in"}}]}

    User: Type hello into the search box
    {"actions": [{"handler": "BROWSER", "operation": "TYPE", "parameters": {"selector": "search box", "text": "hello"}}]}

    User: Press Enter
    {"actions": [{"handler": "BROWSER", "operation": "PRESS", "parameters": {"key": "ENTER"}}]}

    User: Scroll down 600 pixels
    {"actions": [{"handler": "BROWSER", "operation": "SCROLL", "parameters": {"pixels": 600}}]}

    User: Select Nigeria from the country dropdown
    {"actions": [{"handler": "BROWSER", "operation": "SELECT", "parameters": {"selector": "country", "value": "Nigeria"}}]}

    User: Upload C:\\work\\report.pdf using the resume input
    {"actions": [{"handler": "BROWSER", "operation": "UPLOAD_FILE", "parameters": {"selector": "resume", "path": "C:\\work\\report.pdf"}}]}

    User: Remember that my preferred editor is VS Code
    {"actions": [{"handler": "MEMORY", "operation": "SAVE", "parameters": {"category": "preference", "key": "preferred editor", "value": "VS Code"}}]}

    User: Create a folder named notes
    {"actions": [{"handler": "FILESYSTEM", "operation": "CREATE_DIRECTORY", "parameters": {"path": "notes"}}]}
    """
).strip()
