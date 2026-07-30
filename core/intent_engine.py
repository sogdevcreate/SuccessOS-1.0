"""
Intent engine.
"""

from __future__ import annotations

from models.context import Context
from models.execution_plan import ExecutionPlan


class IntentEngine:
    """
    Converts a Context into an ExecutionPlan.

    Concrete implementations will integrate with an AI provider
    to understand the user's request and build an execution plan.
    """

    def build_plan(self, context: Context) -> ExecutionPlan:
        """
        Build an execution plan from the provided context.
        """
        raise NotImplementedError(
            "IntentEngine.build_plan() has not been implemented."
        )