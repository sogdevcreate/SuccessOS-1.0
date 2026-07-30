"""
Interpreter.
"""

from __future__ import annotations


class Interpreter:
    """
    Normalizes raw user input before it enters the execution pipeline.
    """

    def interpret(self, user_input: str) -> str:
        """
        Normalize whitespace while preserving the user's text.
        """
        return " ".join(user_input.strip().split())