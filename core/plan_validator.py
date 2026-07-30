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