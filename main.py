"""
SuccessOS 1.0

Application entry point.
"""

from __future__ import annotations

from core.application import Application


def main() -> None:
    """
    Application entry point.
    """

    application = Application()
    application.run()


if __name__ == "__main__":
    main()