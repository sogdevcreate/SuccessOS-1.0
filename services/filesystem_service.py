"""
Filesystem Service.

Defines the business operations for filesystem management.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class FilesystemService(ABC):
    """
    Contract for filesystem operations.
    """

    @abstractmethod
    def exists(
        self,
        path: Path,
    ) -> bool:
        """
        Determine whether a file or directory exists.
        """
        raise NotImplementedError

    @abstractmethod
    def read_text(
        self,
        path: Path,
    ) -> str:
        """
        Read a UTF-8 text file.
        """
        raise NotImplementedError

    @abstractmethod
    def write_text(
        self,
        path: Path,
        content: str,
    ) -> bool:
        """
        Write a UTF-8 text file.
        """
        raise NotImplementedError

    @abstractmethod
    def list_directory(
        self,
        path: Path,
    ) -> list[Path]:
        """
        List the contents of a directory.
        """
        raise NotImplementedError

    @abstractmethod
    def create_directory(
        self,
        path: Path,
    ) -> bool:
        """
        Create a directory.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        path: Path,
    ) -> bool:
        """
        Delete a file or directory.
        """
        raise NotImplementedError

    @abstractmethod
    def copy(
        self,
        source: Path,
        destination: Path,
    ) -> bool:
        """
        Copy a file or directory.
        """
        raise NotImplementedError

    @abstractmethod
    def move(
        self,
        source: Path,
        destination: Path,
    ) -> bool:
        """
        Move or rename a file or directory.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        directory: Path,
        pattern: str,
    ) -> list[Path]:
        """
        Search for files matching a pattern.
        """
        raise NotImplementedError