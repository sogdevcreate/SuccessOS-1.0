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
                category TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                metadata TEXT NOT NULL,
                PRIMARY KEY (category, key)
            )
            """
        )

        cursor.execute("PRAGMA table_info(memories)")
        primary_key_columns = [
            row["name"]
            for row in sorted(cursor.fetchall(), key=lambda row: row["pk"])
            if row["pk"]
        ]

        if primary_key_columns != ["category", "key"]:
            cursor.execute(
                """
                CREATE TABLE memories_migrated (
                    category TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    PRIMARY KEY (category, key)
                )
                """
            )
            cursor.execute(
                """
                INSERT INTO memories_migrated (
                    category, key, value, created_at, updated_at, metadata
                )
                SELECT category, key, value, created_at, updated_at, metadata
                FROM memories
                """
            )
            cursor.execute("DROP TABLE memories")
            cursor.execute("ALTER TABLE memories_migrated RENAME TO memories")
            self._logger.info("Migrated memory schema to composite primary key.")

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
                INSERT INTO memories (
                    category,
                    key,
                    value,
                    created_at,
                    updated_at,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(category, key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at,
                    metadata = excluded.metadata
                """,
                (
                    memory.category.value,
                    memory.key,
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

    def list(self) -> list[MemoryRecord]:
        """Return all memories in stable category/key order."""

        try:
            cursor = self._database.connection.cursor()
            cursor.execute(
                """
                SELECT key, category, value, created_at, updated_at, metadata
                FROM memories
                ORDER BY category, key
                """
            )

            return [
                MemoryRecord(
                    category=MemoryCategory(row["category"]),
                    key=row["key"],
                    value=json.loads(row["value"]),
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"]),
                    metadata=json.loads(row["metadata"]),
                )
                for row in cursor.fetchall()
            ]

        except Exception as ex:
            self._logger.error(f"Failed to list memories: {ex}")
            return []
