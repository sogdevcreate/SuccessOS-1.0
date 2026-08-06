from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from infrastructure.filesystem.filesystem_sandbox import (
    FilesystemAccessError,
    FilesystemSandbox,
)
from infrastructure.filesystem.windows_filesystem_service import (
    WindowsFilesystemService,
)


class FilesystemSandboxTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary_directory.name) / "workspace"
        self.outside = Path(self._temporary_directory.name) / "outside"
        self.root.mkdir()
        self.outside.mkdir()
        self.sandbox = FilesystemSandbox([self.root])

    def tearDown(self) -> None:
        self._temporary_directory.cleanup()

    def test_resolve_canonicalizes_a_path_inside_the_root(self) -> None:
        path = self.root / "folder" / ".." / "note.txt"

        self.assertEqual(
            self.sandbox.resolve(path),
            (self.root / "note.txt").resolve(),
        )

    def test_resolve_rejects_directory_traversal(self) -> None:
        path = self.root / ".." / "outside" / "secret.txt"

        with self.assertRaises(FilesystemAccessError):
            self.sandbox.resolve(path)

    def test_resolve_rejects_absolute_path_outside_root(self) -> None:
        with self.assertRaises(FilesystemAccessError):
            self.sandbox.resolve(self.outside / "secret.txt")

    def test_multiple_configured_roots_are_allowed(self) -> None:
        extra_root = self.outside / "approved"
        extra_root.mkdir()
        sandbox = FilesystemSandbox([self.root, extra_root])

        self.assertEqual(
            sandbox.resolve(extra_root / "note.txt"),
            (extra_root / "note.txt").resolve(),
        )

    def test_empty_roots_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            FilesystemSandbox([])

    def test_symlink_escape_is_rejected(self) -> None:
        link = self.root / "outside-link"

        try:
            os.symlink(self.outside, link, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"Symlinks are unavailable: {error}")

        with self.assertRaises(FilesystemAccessError):
            self.sandbox.resolve(link / "secret.txt")

    def test_canonical_symlink_escape_is_rejected(self) -> None:
        candidate = self.root / "outside-link" / "secret.txt"
        escaped_path = (self.outside / "secret.txt").resolve()
        original_resolve = Path.resolve

        def resolve(path: Path, strict: bool = False) -> Path:
            if path == candidate:
                return escaped_path
            return original_resolve(path, strict=strict)

        with patch.object(Path, "resolve", autospec=True, side_effect=resolve):
            with self.assertRaises(FilesystemAccessError):
                self.sandbox.resolve(candidate)


class WindowsFilesystemServiceSandboxTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary_directory.name) / "workspace"
        self.outside = Path(self._temporary_directory.name) / "outside"
        self.root.mkdir()
        self.outside.mkdir()
        self.service = WindowsFilesystemService([self.root])

    def tearDown(self) -> None:
        self._temporary_directory.cleanup()

    def test_allows_read_write_and_search_inside_root(self) -> None:
        nested = self.root / "notes"
        self.service.create_directory(nested)
        target = nested / "todo.txt"

        self.service.write_text(target, "finish sandbox")

        self.assertTrue(self.service.exists(target))
        self.assertEqual(self.service.read_text(target), "finish sandbox")
        self.assertEqual(self.service.search(self.root, "*.txt"), [target])

    def test_allows_copy_move_and_delete_inside_root(self) -> None:
        source = self.root / "source.txt"
        copied = self.root / "copied.txt"
        moved = self.root / "moved.txt"
        self.service.write_text(source, "safe")

        self.service.copy(source, copied)
        self.service.move(copied, moved)
        self.service.delete(moved)

        self.assertTrue(source.exists())
        self.assertFalse(copied.exists())
        self.assertFalse(moved.exists())

    def test_rejects_outside_paths_for_all_operations(self) -> None:
        source = self.root / "source.txt"
        self.service.write_text(source, "safe")
        outside = self.outside / "outside.txt"

        operations = (
            lambda: self.service.exists(outside),
            lambda: self.service.read_text(outside),
            lambda: self.service.write_text(outside, "blocked"),
            lambda: self.service.list_directory(self.outside),
            lambda: self.service.create_directory(self.outside / "new"),
            lambda: self.service.delete(outside),
            lambda: self.service.copy(source, outside),
            lambda: self.service.copy(outside, self.root / "copy.txt"),
            lambda: self.service.move(source, outside),
            lambda: self.service.move(outside, self.root / "moved.txt"),
            lambda: self.service.search(self.outside, "*.txt"),
        )

        for operation in operations:
            with self.subTest(operation=operation):
                with self.assertRaises(FilesystemAccessError):
                    operation()

    def test_listing_rejects_symlinks_that_escape_the_root(self) -> None:
        link = self.root / "outside-link"

        try:
            os.symlink(self.outside, link, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"Symlinks are unavailable: {error}")

        with self.assertRaises(FilesystemAccessError):
            self.service.list_directory(self.root)


if __name__ == "__main__":
    unittest.main()
