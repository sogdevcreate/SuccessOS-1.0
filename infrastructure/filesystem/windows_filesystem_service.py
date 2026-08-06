"""
Windows Filesystem Service.

Windows implementation of the FilesystemService contract.
"""

from __future__ import annotations

import shutil
from collections.abc import Iterable
from pathlib import Path

from infrastructure.filesystem.filesystem_sandbox import (
    FilesystemSandbox,
)
from services.filesystem_service import FilesystemService


class WindowsFilesystemService(FilesystemService):
    """
    Windows implementation of filesystem operations.
    """

    def __init__(
        self,
        allowed_roots: Iterable[str | Path] | None = None,
    ) -> None:
        if allowed_roots is None:
            allowed_roots = (Path.cwd(),)

        self._sandbox = FilesystemSandbox(allowed_roots)

    def exists(
        self,
        path: Path,
    ) -> bool:
        return self._sandbox.resolve(path).exists()

    def read_text(
        self,
        path: Path,
    ) -> str:
        return self._sandbox.resolve(path).read_text(
            encoding="utf-8",
        )

    def write_text(
        self,
        path: Path,
        content: str,
    ) -> bool:
        self._sandbox.resolve(path).write_text(
            content,
            encoding="utf-8",
        )
        return True

    def list_directory(
        self,
        path: Path,
    ) -> list[Path]:
        directory = self._sandbox.resolve(path)
        return sorted(
            self._sandbox.resolve(item)
            for item in directory.iterdir()
        )

    def create_directory(
        self,
        path: Path,
    ) -> bool:
        self._sandbox.resolve(path).mkdir(
            parents=True,
            exist_ok=True,
        )
        return True

    def delete(
        self,
        path: Path,
    ) -> bool:
        target = self._sandbox.resolve(path)

        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()

        return True

    def copy(
        self,
        source: Path,
        destination: Path,
    ) -> bool:
        source_path = self._sandbox.resolve(source)
        destination_path = self._sandbox.resolve(destination)

        if source_path.is_dir():
            shutil.copytree(
                source_path,
                destination_path,
                dirs_exist_ok=True,
            )
        else:
            shutil.copy2(
                source_path,
                destination_path,
            )

        return True

    def move(
        self,
        source: Path,
        destination: Path,
    ) -> bool:
        source_path = self._sandbox.resolve(source)
        destination_path = self._sandbox.resolve(destination)

        shutil.move(str(source_path), str(destination_path))
        return True

    def search(
        self,
        directory: Path,
        pattern: str,
    ) -> list[Path]:
        search_root = self._sandbox.resolve(directory)
        return sorted(
            self._sandbox.resolve(path)
            for path in search_root.rglob(pattern)
        )
