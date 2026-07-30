"""
Profile Service.

Defines the business operations for user profile management.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from models.user_profile import UserProfile


class ProfileService(ABC):
    """
    Contract for user profile operations.
    """

    @abstractmethod
    def get_profile(self) -> UserProfile | None:
        """
        Retrieve the current user profile.
        """
        raise NotImplementedError

    @abstractmethod
    def save_profile(
        self,
        profile: UserProfile,
    ) -> bool:
        """
        Save the user profile.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_profile(self) -> bool:
        """
        Delete the current user profile.
        """
        raise NotImplementedError