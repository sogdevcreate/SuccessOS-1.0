"""
JSON Profile Service.

JSON implementation of the ProfileService contract.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from models.user_profile import UserProfile
from services.profile_service import ProfileService


class JsonProfileService(ProfileService):
    """
    JSON implementation of user profile storage.
    """

    def __init__(
        self,
        profile_path: str = "data/profile.json",
    ) -> None:
        self._profile_path = Path(profile_path)

        self._profile_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def get_profile(self) -> UserProfile | None:
        """
        Retrieve the user profile.
        """

        if not self._profile_path.exists():
            return None

        try:
            with self._profile_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            return UserProfile(**data)

        except Exception:
            return None

    def save_profile(
        self,
        profile: UserProfile,
    ) -> bool:
        """
        Save the user profile.
        """

        try:
            with self._profile_path.open(
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    asdict(profile),
                    file,
                    indent=4,
                )

            return True

        except Exception:
            return False

    def delete_profile(self) -> bool:
        """
        Delete the stored user profile.
        """

        try:
            if self._profile_path.exists():
                self._profile_path.unlink()

            return True

        except Exception:
            return False