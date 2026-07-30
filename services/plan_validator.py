"""
Plan validator service contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PlanValidator(ABC):
    """
    Validates AI-generated execution plans.
    """

    @abstractmethod
    def validate(
        self,
        data: dict,
    ) -> None:
        """
        Validate a raw execution plan.

        Raises:
            ValueError: If the plan is invalid.
        """
        raise NotImplementedError