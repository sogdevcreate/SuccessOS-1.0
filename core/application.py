"""
Application.

Coordinates the lifecycle of SuccessOS.
"""

from __future__ import annotations

from config.service_container import ServiceContainer


class Application:
    """
    Main application.

    Owns the application lifecycle.
    """

    def __init__(self) -> None:
        self._container = ServiceContainer()
        self._logger = self._container.logging_service

    @property
    def container(self) -> ServiceContainer:
        return self._container

    @property
    def planner(self):
        return self._container.planner

    @property
    def plan_validator(self):
        return self._container.plan_validator

    @property
    def execution_engine(self):
        return self._container.execution_engine

    def start(self) -> None:
        """
        Start the application.
        """

        self._logger.info("Starting SuccessOS 1.0.")

        print("SuccessOS 1.0 initialized successfully.")
        print("Type 'exit' to quit.\n")

        self._logger.info("SuccessOS 1.0 started successfully.")

    def shutdown(self) -> None:
        """
        Shutdown the application.
        """

        self._logger.info("Shutting down SuccessOS 1.0.")

    def run(self) -> None:
        """
        Run the application.
        """

        try:
            self.start()

            while True:

                prompt = input("> ").strip()

                if not prompt:
                    continue

                if prompt.lower() in {"exit", "quit"}:
                    break

                try:
                    plan = self.planner.create_plan(prompt)

                    self.plan_validator.validate(plan)

                    result = self.execution_engine.execute(plan)

                    print(result.message)

                except Exception as ex:
                    self._logger.exception(
                        "Command execution failed."
                    )

                    print(f"\nError: {ex}\n")

        finally:
            self.shutdown()