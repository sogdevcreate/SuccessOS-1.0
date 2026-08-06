"""Central browser safety policy."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from urllib.parse import SplitResult, urlsplit, urlunsplit


class BrowserPolicyError(PermissionError):
    """Raised when a browser operation violates the configured policy."""


ConfirmationProvider = Callable[[str], bool]


class BrowserPolicyManager:
    """Validate browser destinations and authorize sensitive browser input."""

    _LOCAL_PATH = re.compile(
        r"^(?:[a-zA-Z]:[\\/]|\\\\|/|~[\\/])"
    )

    def __init__(
        self,
        allowed_domains: Iterable[str] = (),
        allowed_schemes: Iterable[str] = ("https",),
        confirmation_provider: ConfirmationProvider | None = None,
    ) -> None:
        self._allowed_domains = tuple(
            self._normalize_domain(domain)
            for domain in allowed_domains
        )
        self._allowed_schemes = frozenset(
            scheme.lower().rstrip(":")
            for scheme in allowed_schemes
        )
        self._confirmation_provider = (
            confirmation_provider or self._request_confirmation
        )

        if not self._allowed_schemes:
            raise ValueError("At least one browser URL scheme is required.")

    @property
    def allowed_domains(self) -> tuple[str, ...]:
        """Return domains permitted for HTTP(S) navigation."""

        return self._allowed_domains

    @property
    def allowed_schemes(self) -> frozenset[str]:
        """Return URL schemes explicitly permitted for navigation."""

        return self._allowed_schemes

    def authorize_navigation(self, url: str) -> str:
        """Validate, normalize, and authorize a navigation URL."""

        normalized = self.normalize_url(url)
        parts = urlsplit(normalized)

        if parts.scheme in {"http", "https"}:
            host = parts.hostname
            if host is None or not self._is_allowed_domain(host):
                raise BrowserPolicyError(
                    f"Navigation to '{host or url}' is not allowed."
                )

        return normalized

    def normalize_url(self, url: str) -> str:
        """Return a canonical URL after validating its scheme and structure."""

        if not isinstance(url, str) or not url.strip():
            raise BrowserPolicyError("A non-empty URL is required.")

        candidate = url.strip()

        if any(character.isspace() for character in candidate):
            raise BrowserPolicyError("URLs cannot contain whitespace.")

        parts = urlsplit(candidate)
        scheme = parts.scheme.lower()

        if scheme not in self._allowed_schemes:
            raise BrowserPolicyError(
                f"URL scheme '{scheme or 'missing'}' is not allowed."
            )

        if scheme in {"http", "https"}:
            return self._normalize_web_url(parts, scheme)

        return urlunsplit(
            (
                scheme,
                parts.netloc,
                parts.path,
                parts.query,
                parts.fragment,
            )
        )

    def authorize_upload(self, path: str) -> None:
        """Require confirmation before a local file is uploaded."""

        if not self._confirmation_provider(f"Upload local file '{path}'"):
            raise BrowserPolicyError("File upload was not authorized by the user.")

    def authorize_form_submission(self, values: Iterable[str]) -> None:
        """Require confirmation when submitted form values include local paths."""

        if not any(self.contains_local_file_path(value) for value in values):
            return

        if not self._confirmation_provider(
            "Submit a form containing a local file path"
        ):
            raise BrowserPolicyError(
                "Form submission containing a local file path was not authorized."
            )

    def contains_local_file_path(self, value: str) -> bool:
        """Return whether a value resembles a local Windows or POSIX path."""

        return isinstance(value, str) and bool(
            self._LOCAL_PATH.match(value.strip())
        )

    def _is_allowed_domain(self, host: str) -> bool:
        normalized_host = host.rstrip(".").lower()

        return any(
            normalized_host == domain
            or normalized_host.endswith(f".{domain}")
            for domain in self._allowed_domains
        )

    @staticmethod
    def _normalize_domain(domain: str) -> str:
        normalized = domain.strip().lower().lstrip("*.").rstrip(".")

        if not normalized or "/" in normalized or ":" in normalized:
            raise ValueError(f"Invalid allowed domain: '{domain}'.")

        return normalized

    @staticmethod
    def _normalize_web_url(parts: SplitResult, scheme: str) -> str:
        if not parts.hostname:
            raise BrowserPolicyError("HTTP(S) URLs must include a hostname.")

        if parts.username is not None or parts.password is not None:
            raise BrowserPolicyError("URLs cannot include user credentials.")

        try:
            port = parts.port
        except ValueError as error:
            raise BrowserPolicyError("URL contains an invalid port.") from error

        host = parts.hostname.rstrip(".").lower()
        if ":" in host:
            host = f"[{host}]"

        netloc = host if port is None else f"{host}:{port}"

        return urlunsplit(
            (
                scheme,
                netloc,
                parts.path or "/",
                parts.query,
                parts.fragment,
            )
        )

    @staticmethod
    def _request_confirmation(message: str) -> bool:
        try:
            return input(f"Allow browser action: {message}? [y/N]: ").strip().lower() in {
                "y",
                "yes",
            }
        except EOFError:
            return False
