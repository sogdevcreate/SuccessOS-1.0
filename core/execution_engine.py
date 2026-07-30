"""
Execution Engine.
"""

from __future__ import annotations

from core.router import Router
from models.execution_plan import ExecutionPlan
from models.execution_result import ExecutionResult


class ExecutionEngine:
    """
    Executes an execution plan.
    """

    def __init__(
        self,
        router: Router,
    ) -> None:
        self._router = router

    def execute(
        self,
        plan: ExecutionPlan,
    ) -> ExecutionResult:
        """
        Execute an execution plan.
        """

        total = len(plan)
        completed = 0

        last_result: ExecutionResult | None = None

        for action in plan:

            result = self._router.route(action)

            if not result.successful:
                return ExecutionResult(
                    status=result.status,
                    message=result.message,
                    payload=result.payload,
                    completed_actions=completed,
                    total_actions=total,
                    errors=result.errors,
                    metadata=result.metadata,
                )

            completed += 1
            last_result = result

        if last_result is None:
            return ExecutionResult.fail(
                message="Execution plan contained no actions."
            )

        return ExecutionResult(
            status=last_result.status,
            message=last_result.message,
            payload=last_result.payload,
            completed_actions=completed,
            total_actions=total,
            errors=last_result.errors,
            metadata=last_result.metadata,
        )