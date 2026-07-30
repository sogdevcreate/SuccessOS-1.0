"""
Windows Filesystem Service.

Windows implementation of the FilesystemService contract.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from services.filesystem_service import FilesystemService


class WindowsFilesystemService(FilesystemService):
    """
    Windows implementation of filesystem operations.
    """

    def exists(
        self,
        path: Path,
    ) -> bool:
        return path.exists()

    def read_text(
        self,
        path: Path,
    ) -> str:
        return path.read_text(
            encoding="utf-8",
        )

    def write_text(
        self,
        path: Path,
        content: str,
    ) -> bool:
        path.write_text(
            content,
            encoding="utf-8",
        )
        return True

    def list_directory(
        self,
        path: Path,
    ) -> list[Path]:
        return sorted(path.iterdir())

    def create_directory(
        self,
        path: Path,
    ) -> bool:
        path.mkdir(
            parents=True,
            exist_ok=True,
        )
        return True

    def delete(
        self,
        path: Path,
    ) -> bool:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()

        return True

    def copy(
        self,
        source: Path,
        destination: Path,
    ) -> bool:
        if source.is_dir():
            shutil.copytree(
                source,
                destination,
                dirs_exist_ok=True,
            )
        else:
            shutil.copy2(
                source,
                destination,
            )

        return True

    def move(
        self,
        source: Path,
        destination: Path,
    ) -> bool:
        shutil.move(
            str(source),
            str(destination),
        )
        return True

    def search(
        self,
        directory: Path,
        pattern: str,
    ) -> list[Path]:
        return sorted(directory.rglob(pattern))