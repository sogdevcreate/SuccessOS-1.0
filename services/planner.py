"""
Planner service contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from models.execution_plan import ExecutionPlan


class Planner(ABC):
    """
    Builds an execution plan from user input.
    """

    @abstractmethod
    def create_plan(
        self,
        prompt: str,
    ) -> ExecutionPlan:
        """
        Generate an execution plan.
        """
        raise NotImplementedError