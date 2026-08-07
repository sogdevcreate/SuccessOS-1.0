"""Raised when a plan cannot be safely understood or validated."""

from __future__ import annotations


class ClarificationRequiredError(Exception):
    """Provide a safe user-facing recovery message for invalid AI plans."""

    def __init__(self, message: str = "I could not safely interpret that request. Please clarify it and try again.") -> None:
        super().__init__(message)
