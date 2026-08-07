"""
Execution Engine.
"""

from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter

from core.permission_manager import PermissionManager
from core.router import Router
from models.execution_plan import ExecutionPlan
from models.execution_result import ExecutionResult
from models.execution_trace_entry import ExecutionTraceEntry


class ExecutionEngine:
    """
    Executes an execution plan.
    """

    def __init__(
        self,
        router: Router,
        permission_manager: PermissionManager | None = None,
    ) -> None:
        self._router = router
        self._permission_manager = (
            permission_manager or PermissionManager()
        )

    def execute(
        self,
        plan: ExecutionPlan,
    ) -> ExecutionResult:
        """
        Execute an execution plan.
        """

        total = len(plan)
        completed = 0
        trace: list[ExecutionTraceEntry] = []

        last_result: ExecutionResult | None = None

        for action in plan:

            started_at = datetime.now(timezone.utc)
            started = perf_counter()

            try:
                permission_result = self._permission_manager.authorize(
                    action,
                )

                if permission_result is not None:
                    trace.append(self._trace_entry(
                        action,
                        started_at,
                        started,
                        permission_result,
                    ))
                    return self._with_progress(
                        permission_result,
                        completed,
                        total,
                        trace,
                    )

                result = self._router.route(action)

                trace.append(self._trace_entry(
                    action,
                    started_at,
                    started,
                    result,
                ))

                if not result.successful:
                    return self._with_progress(
                        result,
                        completed,
                        total,
                        trace,
                    )

            except Exception as ex:
                result = ExecutionResult.fail(
                    message=str(ex),
                    errors=[str(ex)],
                )
                trace.append(self._trace_entry(
                    action,
                    started_at,
                    started,
                    result,
                ))
                return self._with_progress(
                    result,
                    completed,
                    total,
                    trace,
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
            trace=trace,
        )

    @staticmethod
    def _trace_entry(
        action,
        started_at: datetime,
        started: float,
        result: ExecutionResult,
    ) -> ExecutionTraceEntry:
        ended_at = datetime.now(timezone.utc)

        return ExecutionTraceEntry(
            action_name=action.name,
            handler=action.handler,
            operation=action.operation,
            started_at=started_at,
            ended_at=ended_at,
            duration_seconds=perf_counter() - started,
            status=result.status,
            error="; ".join(result.errors) or (
                result.message if not result.successful else ""
            ),
        )

    @staticmethod
    def _with_progress(
        result: ExecutionResult,
        completed: int,
        total: int,
        trace: list[ExecutionTraceEntry],
    ) -> ExecutionResult:
        return ExecutionResult(
            status=result.status,
            message=result.message,
            payload=result.payload,
            completed_actions=completed,
            total_actions=total,
            errors=result.errors,
            metadata=result.metadata,
            trace=trace,
        )
