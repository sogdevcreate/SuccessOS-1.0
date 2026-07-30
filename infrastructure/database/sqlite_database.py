"""
SQLite Database.

Provides a shared SQLite connection for infrastructure services.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


class SQLiteDatabase:
    """
    Manages the application's SQLite database.
    """

    def __init__(
        self,
        database_path: str = "data/successos.db",
    ) -> None:
        self._database_path = Path(database_path)

        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._connection = sqlite3.connect(
            self._database_path,
            check_same_thread=False,
        )

        self._connection.row_factory = sqlite3.Row

    @property
    def connection(self) -> sqlite3.Connection:
        """
        Return the SQLite connection.
        """

        return self._connection

    def close(self) -> None:
        """
        Close the database connection.
        """

        self._connection.close()