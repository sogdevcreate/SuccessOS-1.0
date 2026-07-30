"""
SuccessOS System Status Model

Represents the current state of the computer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SystemStatus:
    """
    Represents basic system information.
    """

    cpu_usage: float = 0.0

    memory_usage: float = 0.0

    disk_usage: float = 0.0

    network_connected: bool = True