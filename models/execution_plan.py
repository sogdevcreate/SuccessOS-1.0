"""
Execution Plan.

Represents an ordered collection of executable actions.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from models.action import Action


@dataclass(slots=True)
class ExecutionPlan:
    """
    Ordered collection of executable actions.
    """

    actions: list[Action] = field(default_factory=list)

    def add(self, action: Action) -> None:
        """
        Add an action to the execution plan.
        """
        self.actions.append(action)

    @property
    def empty(self) -> bool:
        """
        Returns True if the execution plan contains no actions.
        """
        return not self.actions

    def __len__(self) -> int:
        return len(self.actions)

    def __iter__(self):
        return iter(self.actions)