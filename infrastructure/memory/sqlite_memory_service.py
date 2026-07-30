"""
SQLite Memory Service.

SQLite implementation of the MemoryService contract.
"""

from __future__ import annotations

import json
from datetime import datetime

from enums.memory_category import MemoryCategory
from infrastructure.database.sqlite_database import SQLiteDatabase
from models.memory_record import MemoryRecord
from services.logging_service import LoggingService
from services.memory_service import MemoryService


class SQLiteMemoryService(MemoryService):
    """
    SQLite implementation of assistant memory.
    """

    def __init__(
        self,
        database: SQLiteDatabase,
        logger: LoggingService,
    ) -> None:
        self._database = database
        self._logger = logger
        self._create_table()

    def _create_table(self) -> None:
        """
        Create the memory table if it does not exist.
        """

        cursor = self._database.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                key TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                value TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                metadata TEXT NOT NULL
            )
            """
        )

        self._database.connection.commit()

        self._logger.info("Memory table initialized.")

    def remember(
        self,
        memory: MemoryRecord,
    ) -> bool:
        """
        Store or update a memory.
        """

        try:
            cursor = self._database.connection.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO memories (
                    key,
                    category,
                    value,
                    created_at,
                    updated_at,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    memory.key,
                    memory.category.value,
                    json.dumps(memory.value),
                    memory.created_at.isoformat(),
                    memory.updated_at.isoformat(),
                    json.dumps(memory.metadata),
                ),
            )

            self._database.connection.commit()

            self._logger.info(
                f"Stored memory '{memory.key}'."
            )

            return True

        except Exception as ex:
            self._logger.error(
                f"Failed to store memory '{memory.key}': {ex}"
            )
            return False

    def recall(
        self,
        category: MemoryCategory,
        key: str,
    ) -> MemoryRecord | None:
        """
        Retrieve a specific memory.
        """

        try:
            cursor = self._database.connection.cursor()

            cursor.execute(
                """
                SELECT
                    key,
                    category,
                    value,
                    created_at,
                    updated_at,
                    metadata
                FROM memories
                WHERE category = ?
                  AND key = ?
                LIMIT 1
                """,
                (
                    category.value,
                    key,
                ),
            )

            row = cursor.fetchone()

            if row is None:
                self._logger.info(
                    f"Memory '{key}' was not found."
                )
                return None

            memory = MemoryRecord(
                category=MemoryCategory(row["category"]),
                key=row["key"],
                value=json.loads(row["value"]),
                created_at=datetime.fromisoformat(
                    row["created_at"]
                ),
                updated_at=datetime.fromisoformat(
                    row["updated_at"]
                ),
                metadata=json.loads(row["metadata"]),
            )

            self._logger.info(
                f"Retrieved memory '{key}'."
            )

            return memory

        except Exception as ex:
            self._logger.error(
                f"Failed to retrieve memory '{key}': {ex}"
            )
            return None

    def forget(
        self,
        category: MemoryCategory,
        key: str,
    ) -> bool:
        """
        Remove a specific memory.
        """

        try:
            cursor = self._database.connection.cursor()

            cursor.execute(
                """
                DELETE FROM memories
                WHERE category = ?
                  AND key = ?
                """,
                (
                    category.value,
                    key,
                ),
            )

            self._database.connection.commit()

            removed = cursor.rowcount > 0

            if removed:
                self._logger.info(
                    f"Deleted memory '{key}'."
                )
            else:
                self._logger.warning(
                    f"Memory '{key}' was not found."
                )

            return removed

        except Exception as ex:
            self._logger.error(
                f"Failed to delete memory '{key}': {ex}"
            )
            return False