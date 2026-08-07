from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from enums.memory_category import MemoryCategory
from infrastructure.database.sqlite_database import SQLiteDatabase
from infrastructure.memory.sqlite_memory_service import SQLiteMemoryService
from models.memory_record import MemoryRecord
from tests.helpers.reporting import ComponentTestCase


class _Logger:
    def info(self, message):
        return None

    def warning(self, message):
        return None

    def error(self, message):
        return None


class SQLiteMemoryServiceTests(ComponentTestCase):
    subsystem = "Memory"
    component = "SQLiteMemoryService migration and composite key"
    recommended_location = "infrastructure/memory/sqlite_memory_service.py"

    def test_migrates_legacy_schema_and_keeps_categories_independent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.db"
            legacy = sqlite3.connect(path)
            legacy.execute(
                """
                CREATE TABLE memories (
                    key TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    value TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata TEXT NOT NULL
                )
                """
            )
            legacy.execute(
                "INSERT INTO memories VALUES (?, ?, ?, ?, ?, ?)",
                ("theme", "preference", '"dark"', "2025-01-01T00:00:00", "2025-01-01T00:00:00", "{}"),
            )
            legacy.commit()
            legacy.close()

            database = SQLiteDatabase(str(path))
            service = SQLiteMemoryService(database, _Logger())
            service.remember(MemoryRecord(MemoryCategory.FACT, "theme", "fact value"))
            service.remember(MemoryRecord(MemoryCategory.PREFERENCE, "theme", "light"))
            created_at = service.recall(
                MemoryCategory.PREFERENCE,
                "theme",
            ).created_at
            service.remember(MemoryRecord(MemoryCategory.PREFERENCE, "theme", "updated"))

            self.assertEqual(
                service.recall(MemoryCategory.FACT, "theme").value,
                "fact value",
            )
            self.assertEqual(
                service.recall(MemoryCategory.PREFERENCE, "theme").value,
                "updated",
            )
            self.assertEqual(
                service.recall(
                    MemoryCategory.PREFERENCE,
                    "theme",
                ).created_at,
                created_at,
            )
            self.assertTrue(service.forget(MemoryCategory.FACT, "theme"))
            self.assertIsNone(service.recall(MemoryCategory.FACT, "theme"))
            self.assertEqual(
                service.recall(MemoryCategory.PREFERENCE, "theme").value,
                "updated",
            )
            self.assertEqual(len(service.list()), 1)
            database.close()
