"""Build execution plans using deterministic and AI-backed planning."""

from __future__ import annotations

import json

from enums.handler_type import HandlerType
from enums.operation_type import OperationType
from core.plan_validator import PlanValidator
from exceptions.clarification_required_error import ClarificationRequiredError
from exceptions.plan_validation_error import PlanValidationError
from infrastructure.ai.browser_intent_classifier import (
    BrowserIntentClassifier,
)
from models.action import Action
from models.ai_request import AIRequest
from models.execution_plan import ExecutionPlan
from prompts.system_prompt import SYSTEM_PROMPT
from services.ai_service import AIService
from services.planner import Planner


class AIPlanner(Planner):
    """AI implementation of the Planner contract."""

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        self._ai_service = ai_service
        self._browser_intent_classifier = BrowserIntentClassifier()
        self._plan_validator = PlanValidator()

    def create_plan(
        self,
        prompt: str,
    ) -> ExecutionPlan:
        """Create an execution plan from a natural language prompt."""

        browser_plan = self._browser_intent_classifier.create_plan(prompt)

        if browser_plan is not None:
            return browser_plan

        response = self._ai_service.generate(
            AIRequest(
                system_prompt=SYSTEM_PROMPT,
                prompt=prompt,
                temperature=0,
                max_tokens=500,
            )
        )

        return self._parse_plan(response.content)

    def _parse_plan(self, content: str) -> ExecutionPlan:
        """Parse and strictly validate an AI response before execution."""

        try:
            data = json.loads(content)
        except (TypeError, json.JSONDecodeError) as ex:
            raise ClarificationRequiredError() from ex

        if not isinstance(data, dict) or set(data) != {"actions"}:
            raise ClarificationRequiredError()

        actions_data = data["actions"]

        if not isinstance(actions_data, list) or not actions_data:
            raise ClarificationRequiredError()

        plan = ExecutionPlan()

        try:
            for item in actions_data:
                if (
                    not isinstance(item, dict)
                    or set(item) != {"handler", "operation", "parameters"}
                    or not isinstance(item["handler"], str)
                    or not isinstance(item["operation"], str)
                    or not isinstance(item["parameters"], dict)
                ):
                    raise ClarificationRequiredError()

                plan.add(
                    Action(
                        name=item["operation"],
                        handler=HandlerType[item["handler"]],
                        operation=OperationType[item["operation"]],
                        parameters=item["parameters"],
                    )
                )

            self._plan_validator.validate(plan)

        except (KeyError, PlanValidationError, ValueError) as ex:
            raise ClarificationRequiredError() from ex

        return plan
