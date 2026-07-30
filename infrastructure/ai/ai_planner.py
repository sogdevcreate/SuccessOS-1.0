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

from services.ai_service import AIService
from services.planner import Planner


SYSTEM_PROMPT = """
You are the planning engine for SuccessOS.

Convert the user's request into an execution plan.

Return ONLY valid JSON.

Schema:

{
  "actions": [
    {
      "handler": "<HANDLER>",
      "operation": "<OPERATION>",
      "parameters": {}
    }
  ]
}

Use ONLY the handlers, operations, parameter names and values defined below.

==================================================
APPLICATION
==================================================

Operations:
- OPEN
- CLOSE

Parameters:
{
    "application": "<application name>"
}

==================================================
INSTALLATION
==================================================

Operations:
- INSTALL
- UNINSTALL

Parameters:
{
    "application": "<application name>"
}

==================================================
MEMORY
==================================================

Operations:
- SAVE
- LOAD
- DELETE

Valid categories (use ONLY these values):
- profile
- preference
- fact
- task
- conversation

SAVE

{
    "category": "<profile|preference|fact|task|conversation>",
    "key": "<key>",
    "value": "<value>"
}

LOAD

{
    "category": "<profile|preference|fact|task|conversation>",
    "key": "<key>"
}

DELETE

{
    "category": "<profile|preference|fact|task|conversation>",
    "key": "<key>"
}

==================================================
FILESYSTEM
==================================================

Operations:
- READ
- WRITE
- LIST
- COPY
- MOVE
- DELETE
- SEARCH
- CREATE_DIRECTORY

READ

{
    "path": "<file path>"
}

WRITE

{
    "path": "<file path>",
    "content": "<text>"
}

LIST

{
    "path": "<directory path>"
}

DELETE

{
    "path": "<file or directory path>"
}

COPY

{
    "source": "<source path>",
    "destination": "<destination path>"
}

MOVE

{
    "source": "<source path>",
    "destination": "<destination path>"
}

SEARCH

{
    "directory": "<directory path>",
    "pattern": "<search pattern>"
}

CREATE_DIRECTORY

{
    "path": "<directory path>"
}

==================================================
NEWS
==================================================

Operations:
- SEARCH

Parameters:
{
    "topic": "<news topic>"
}

==================================================
SYSTEM
==================================================

Operations:
- SHUTDOWN
- RESTART
- SLEEP
- LOCK

Parameters:
{}

==================================================
RULES
==================================================

- Never invent handlers.
- Never invent operations.
- Never invent parameter names.
- Never invent memory categories.
- Use "preference", never "preferences".
- Return ONLY valid JSON.
- Handler names must exactly match:
  APPLICATION
  INSTALLATION
  MEMORY
  FILESYSTEM
  NEWS
  SYSTEM
- Operation names must exactly match the supported operations.
"""


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

        data = json.loads(response.content)

        plan = ExecutionPlan()

        for item in data.get("actions", []):
            plan.add(
                Action(
                    name=item["operation"],
                    handler=HandlerType[item["handler"]],
                    operation=OperationType[item["operation"]],
                    parameters=item.get("parameters", {}),
                )
            )

        return plan