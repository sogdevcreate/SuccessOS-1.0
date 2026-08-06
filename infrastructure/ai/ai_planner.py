"""
AI Planner.

Builds an execution plan using the AI service.
"""

from __future__ import annotations

import json

from enums.handler_type import HandlerType
from enums.operation_type import OperationType

from models.action import Action
from models.ai_request import AIRequest
from models.execution_plan import ExecutionPlan

from prompts.system_prompt import SYSTEM_PROMPT

from services.ai_service import AIService
from services.planner import Planner


class AIPlanner(Planner):
    """
    AI implementation of the Planner contract.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        self._ai_service = ai_service

    def create_plan(
        self,
        prompt: str,
    ) -> ExecutionPlan:
        """
        Create an execution plan from a natural language prompt.
        """

        response = self._ai_service.generate(
            AIRequest(
                system_prompt=SYSTEM_PROMPT,
                prompt=prompt,
                temperature=0,
                max_tokens=500,
            )
        )

        data = json.loads(
            response.content,
        )

        plan = ExecutionPlan()

        for item in data.get(
            "actions",
            [],
        ):
            plan.add(
                Action(
                    name=item["operation"],
                    handler=HandlerType[
                        item["handler"]
                    ],
                    operation=OperationType[
                        item["operation"]
                    ],
                    parameters=item.get(
                        "parameters",
                        {},
                    ),
                )
            )

        return plan
