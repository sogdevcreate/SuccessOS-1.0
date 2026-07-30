"""
SuccessOS Action Model

Represents a single executable action in an execution plan.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from enums.handler_type import HandlerType
from enums.operation_type import OperationType
from enums.permission_level import PermissionLevel


@dataclass(slots=True)
class Action:
    """
    Represents a single executable action.

    The Intent Engine creates Action objects.
    The Execution Engine executes them.
    """

    name: str

    handler: HandlerType

    operation: OperationType

    parameters: dict[str, Any] = field(default_factory=dict)

    permission: PermissionLevel = PermissionLevel.NONE

    description: str = ""

    requires_confirmation: bool = False