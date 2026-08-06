"""
Plan Validator.

Validates AI-generated execution plans before execution.
"""

from __future__ import annotations

from enums.handler_type import HandlerType
from enums.operation_type import OperationType
from exceptions.plan_validation_error import PlanValidationError


class PlanValidator:
    """
    Validates execution plans produced by the AI planner.
    """

    _REQUIRED_PARAMETERS = {
        #
        # Application
        #
        (HandlerType.APPLICATION, OperationType.OPEN): (
            "application",
        ),
        (HandlerType.APPLICATION, OperationType.CLOSE): (
            "application",
        ),

        #
        # Installation
        #
        (HandlerType.INSTALLATION, OperationType.INSTALL): (
            "application",
        ),
        (HandlerType.INSTALLATION, OperationType.UNINSTALL): (
            "application",
        ),

        #
        # Memory
        #
        (HandlerType.MEMORY, OperationType.SAVE): (
            "category",
            "key",
            "value",
        ),
        (HandlerType.MEMORY, OperationType.LOAD): (
            "category",
            "key",
        ),
        (HandlerType.MEMORY, OperationType.DELETE): (
            "category",
            "key",
        ),

        #
        # Filesystem
        #
        (HandlerType.FILESYSTEM, OperationType.READ): (
            "path",
        ),
        (HandlerType.FILESYSTEM, OperationType.WRITE): (
            "path",
            "content",
        ),
        (HandlerType.FILESYSTEM, OperationType.LIST): (
            "path",
        ),
        (HandlerType.FILESYSTEM, OperationType.DELETE): (
            "path",
        ),
        (HandlerType.FILESYSTEM, OperationType.COPY): (
            "source",
            "destination",
        ),
        (HandlerType.FILESYSTEM, OperationType.MOVE): (
            "source",
            "destination",
        ),
        (HandlerType.FILESYSTEM, OperationType.SEARCH): (
            "directory",
            "pattern",
        ),
        (HandlerType.FILESYSTEM, OperationType.CREATE_DIRECTORY): (
            "path",
        ),

        #
        # Clipboard
        #
        (HandlerType.CLIPBOARD, OperationType.COPY): (
            "text",
        ),
        (HandlerType.CLIPBOARD, OperationType.READ): (),
        (HandlerType.CLIPBOARD, OperationType.CLEAR): (),

        #
        # Process
        #
        (HandlerType.PROCESS, OperationType.LIST_PROCESSES): (),
        (HandlerType.PROCESS, OperationType.START_PROCESS): (
            "command",
        ),
        (HandlerType.PROCESS, OperationType.KILL_PROCESS): (
            "process",
        ),
        (HandlerType.PROCESS, OperationType.PROCESS_INFO): (
            "process",
        ),

        #
        # Browser
        #
        (HandlerType.BROWSER, OperationType.OPEN_URL): (
            "url",
        ),
        (HandlerType.BROWSER, OperationType.OPEN_TAB): (
            "url",
        ),
        (HandlerType.BROWSER, OperationType.CLOSE_TAB): (),
        (HandlerType.BROWSER, OperationType.REFRESH_PAGE): (),
        (HandlerType.BROWSER, OperationType.GO_BACK): (),
        (HandlerType.BROWSER, OperationType.GO_FORWARD): (),
        (HandlerType.BROWSER, OperationType.LIST_TABS): (),
        (HandlerType.BROWSER, OperationType.CURRENT_TAB): (),
        (HandlerType.BROWSER, OperationType.SWITCH_TAB): (
            "index",
        ),
        (HandlerType.BROWSER, OperationType.PAGE_TITLE): (),
        (HandlerType.BROWSER, OperationType.CLICK): (
            "selector",
        ),
        (HandlerType.BROWSER, OperationType.TYPE): (
            "selector",
            "text",
        ),
        (HandlerType.BROWSER, OperationType.PRESS): (
            "key",
        ),
        (HandlerType.BROWSER, OperationType.WAIT_FOR): (
            "selector",
        ),
        (HandlerType.BROWSER, OperationType.SCROLL): (
            "pixels",
        ),
        (HandlerType.BROWSER, OperationType.SELECT): (
            "selector",
            "value",
        ),
        (HandlerType.BROWSER, OperationType.UPLOAD_FILE): (
            "selector",
            "path",
        ),
        (HandlerType.BROWSER, OperationType.SCREENSHOT): (
            "path",
        ),
        (HandlerType.BROWSER, OperationType.YOUTUBE_SEARCH): (
            "query",
        ),
        (HandlerType.BROWSER, OperationType.YOUTUBE_PLAY): (
            "query",
        ),
        (HandlerType.BROWSER, OperationType.YOUTUBE_VIDEO): (
            "video_id",
        ),
        (HandlerType.BROWSER, OperationType.YOUTUBE_PLAYLIST): (
            "playlist_id",
        ),
        (HandlerType.BROWSER, OperationType.YOUTUBE_CHANNEL): (
            "channel",
        ),

        (HandlerType.BROWSER, OperationType.STUDIO_OPEN): (),
        (HandlerType.BROWSER, OperationType.STUDIO_DASHBOARD): (),
        (HandlerType.BROWSER, OperationType.STUDIO_CONTENT): (),
        (HandlerType.BROWSER, OperationType.STUDIO_ANALYTICS): (),
        (HandlerType.BROWSER, OperationType.STUDIO_COMMENTS): (),
        (HandlerType.BROWSER, OperationType.STUDIO_COPYRIGHT): (),
        (HandlerType.BROWSER, OperationType.STUDIO_MONETIZATION): (),
        (HandlerType.BROWSER, OperationType.STUDIO_SETTINGS): (),

        #
        # News
        #
        (HandlerType.NEWS, OperationType.SEARCH): (
            "topic",
        ),

        #
        # System
        #
        (HandlerType.SYSTEM, OperationType.SHUTDOWN): (),
        (HandlerType.SYSTEM, OperationType.RESTART): (),
        (HandlerType.SYSTEM, OperationType.SLEEP): (),
        (HandlerType.SYSTEM, OperationType.LOCK): (),
    }

    def validate(self, plan) -> None:
        """
        Validate an execution plan.

        Raises:
            PlanValidationError: If the plan is invalid.
        """

        if plan is None:
            raise PlanValidationError(
                "Execution plan is None."
            )

        actions = getattr(plan, "actions", None)

        if not actions:
            raise PlanValidationError(
                "Execution plan contains no actions."
            )

        for index, action in enumerate(
            actions,
            start=1,
        ):
            self._validate_action(
                index,
                action,
            )

    def _validate_action(
        self,
        index: int,
        action,
    ) -> None:
        """
        Validate a single action.
        """

        handler = getattr(
            action,
            "handler",
            None,
        )

        operation = getattr(
            action,
            "operation",
            None,
        )

        if handler is None:
            raise PlanValidationError(
                f"Action {index} is missing a handler."
            )

        if not isinstance(
            handler,
            HandlerType,
        ):
            raise PlanValidationError(
                f"Action {index} has an invalid handler: "
                f"{handler!r}"
            )

        if operation is None:
            raise PlanValidationError(
                f"Action {index} is missing an operation."
            )

        if not isinstance(
            operation,
            OperationType,
        ):
            raise PlanValidationError(
                f"Action {index} has an invalid operation: "
                f"{operation!r}"
            )

        parameters = getattr(
            action,
            "parameters",
            None,
        )

        if parameters is None:
            raise PlanValidationError(
                f"Action {index} is missing a parameters object."
            )

        required = self._REQUIRED_PARAMETERS.get(
            (
                handler,
                operation,
            ),
            (),
        )

        for parameter in required:
            if parameter not in parameters:
                raise PlanValidationError(
                    f"Action {index} is missing required "
                    f"parameter '{parameter}' for "
                    f"{handler.value}/{operation.value}."
                )