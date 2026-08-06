"""Path authorization for filesystem operations."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


class FilesystemAccessError(PermissionError):
    """Raised when a path is outside the approved filesystem roots."""


class FilesystemSandbox:
    """Canonicalize paths and limit them to explicitly approved roots."""

    def __init__(
        self,
        allowed_roots: Iterable[str | Path],
    ) -> None:
        self._allowed_roots = tuple(
            Path(root).resolve(strict=False)
            for root in allowed_roots
        )

        if not self._allowed_roots:
            raise ValueError("At least one filesystem root is required.")

    @property
    def allowed_roots(self) -> tuple[Path, ...]:
        """Return the canonical roots approved for filesystem access."""

        return self._allowed_roots

    def resolve(self, path: str | Path) -> Path:
        """Return a canonical path when it remains inside an approved root."""

        canonical_path = Path(path).resolve(strict=False)

        for root in self._allowed_roots:
            try:
                canonical_path.relative_to(root)
                return canonical_path
            except ValueError:
                continue

        raise FilesystemAccessError(
            f"Filesystem access denied outside approved roots: '{path}'."
        )
