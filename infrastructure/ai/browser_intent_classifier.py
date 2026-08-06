"""Deterministic parsing for concise browser commands."""

from __future__ import annotations

import re

from enums.handler_type import HandlerType
from enums.operation_type import OperationType
from models.action import Action
from models.execution_plan import ExecutionPlan


class BrowserIntentClassifier:
    """Build plans for unambiguous browser imperative commands."""

    _OPEN_NEW_TAB = re.compile(
        r"^open (?:a )?new tab (?P<url>https://\S+)$",
        re.IGNORECASE,
    )
    _OPEN_URL = re.compile(
        r"^open (?P<url>https://\S+)$",
        re.IGNORECASE,
    )
    _CLICK = re.compile(r"^click (?P<selector>.+)$", re.IGNORECASE)
    _TYPE = re.compile(
        r"^type (?P<text>.+?) into (?P<selector>.+)$",
        re.IGNORECASE,
    )
    _PRESS = re.compile(r"^press (?P<key>\S+)$", re.IGNORECASE)
    _SCROLL = re.compile(
        r"^scroll down(?: (?:by )?(?P<pixels>\d+) pixels?)?$",
        re.IGNORECASE,
    )
    _SELECT = re.compile(r"^select (?P<value>.+)$", re.IGNORECASE)
    _UPLOAD = re.compile(
        r"^upload file (?P<path>.+?)(?: (?:to|using) (?P<selector>.+))?$",
        re.IGNORECASE,
    )

    def create_plan(self, prompt: str) -> ExecutionPlan | None:
        """Return a plan for a supported exact browser command."""

        command = prompt.strip()

        for pattern, operation, parameters in (
            (
                self._OPEN_NEW_TAB,
                OperationType.OPEN_TAB,
                lambda match: {"url": match["url"]},
            ),
            (
                self._OPEN_URL,
                OperationType.OPEN_URL,
                lambda match: {"url": match["url"]},
            ),
            (
                self._CLICK,
                OperationType.CLICK,
                lambda match: {"selector": match["selector"]},
            ),
            (
                self._TYPE,
                OperationType.TYPE,
                lambda match: {
                    "selector": match["selector"],
                    "text": match["text"],
                },
            ),
            (
                self._PRESS,
                OperationType.PRESS,
                lambda match: {"key": match["key"].upper()},
            ),
            (
                self._SCROLL,
                OperationType.SCROLL,
                lambda match: {"pixels": int(match["pixels"] or 500)},
            ),
            (
                self._SELECT,
                OperationType.SELECT,
                lambda match: {
                    "selector": "select",
                    "value": match["value"],
                },
            ),
            (
                self._UPLOAD,
                OperationType.UPLOAD_FILE,
                lambda match: {
                    "selector": match["selector"] or "file input",
                    "path": match["path"],
                },
            ),
        ):
            match = pattern.fullmatch(command)

            if match is not None:
                return ExecutionPlan([
                    Action(
                        name=operation.value,
                        handler=HandlerType.BROWSER,
                        operation=operation,
                        parameters=parameters(match),
                    )
                ])

        return None
