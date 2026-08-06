"""
Browser Service.

Defines the contract for browser automation.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BrowserService(ABC):
    """
    Contract for browser automation.
    """

    #
    # Navigation
    #

    @abstractmethod
    def open_url(
        self,
        url: str,
    ) -> None:
        """
        Open a URL.
        """
        ...

    @abstractmethod
    def open_tab(
        self,
        url: str,
    ) -> None:
        """
        Open a URL in a new tab.
        """
        ...

    @abstractmethod
    def close_tab(
        self,
    ) -> None:
        """
        Close the current tab.
        """
        ...

    @abstractmethod
    def refresh_page(
        self,
    ) -> None:
        """
        Refresh the current page.
        """
        ...

    @abstractmethod
    def go_back(
        self,
    ) -> None:
        """
        Navigate back.
        """
        ...

    @abstractmethod
    def go_forward(
        self,
    ) -> None:
        """
        Navigate forward.
        """
        ...

    #
    # Tabs
    #

    @abstractmethod
    def list_tabs(
        self,
    ) -> list[str]:
        """
        Return the titles of all open tabs.
        """
        ...

    @abstractmethod
    def current_tab(
        self,
    ) -> int:
        """
        Return the current tab index.
        """
        ...

    @abstractmethod
    def switch_tab(
        self,
        index: int,
    ) -> None:
        """
        Switch to a browser tab.
        """
        ...

    @abstractmethod
    def page_title(
        self,
    ) -> str:
        """
        Return the current page title.
        """
        ...

    #
    # Interaction
    #

    @abstractmethod
    def click(
        self,
        selector: str,
    ) -> None:
        """
        Click an element.
        """
        ...

    @abstractmethod
    def type(
        self,
        selector: str,
        text: str,
    ) -> None:
        """
        Type into an element.
        """
        ...

    @abstractmethod
    def press(
        self,
        key: str,
    ) -> None:
        """
        Press a keyboard key.
        """
        ...

    @abstractmethod
    def wait_for(
        self,
        selector: str,
        timeout: int = 10,
    ) -> None:
        """
        Wait for an element.
        """
        ...

    @abstractmethod
    def scroll(
        self,
        pixels: int,
    ) -> None:
        """
        Scroll the page.
        """
        ...

    @abstractmethod
    def select(
        self,
        selector: str,
        value: str,
    ) -> None:
        """
        Select an option.
        """
        ...

    @abstractmethod
    def upload_file(
        self,
        selector: str,
        path: str,
    ) -> None:
        """
        Upload a file.
        """
        ...

    @abstractmethod
    def screenshot(
        self,
        path: str,
    ) -> None:
        """
        Save a screenshot.
        """
        ...

    #
    # YouTube
    #

    @abstractmethod
    def youtube_search(
        self,
        query: str,
    ) -> None:
        """
        Search YouTube.
        """
        ...

    @abstractmethod
    def youtube_play(
        self,
        query: str,
    ) -> None:
        """
        Search YouTube and play the first result.
        """
        ...

    @abstractmethod
    def youtube_video(
        self,
        video_id: str,
    ) -> None:
        """
        Open a YouTube video.
        """
        ...

    @abstractmethod
    def youtube_playlist(
        self,
        playlist_id: str,
    ) -> None:
        """
        Open a YouTube playlist.
        """
        ...

    @abstractmethod
    def youtube_channel(
        self,
        channel: str,
    ) -> None:
        """
        Open a YouTube channel.
        """
        ...
        
    #
    # YouTube Studio
    #

    @abstractmethod
    def studio_open(
        self,
    ) -> None:
        """
        Open YouTube Studio.
        """
        ...

    @abstractmethod
    def studio_dashboard(
        self,
    ) -> None:
        """
        Open Studio dashboard.
        """
        ...

    @abstractmethod
    def studio_content(
        self,
    ) -> None:
        """
        Open Studio content.
        """
        ...

    @abstractmethod
    def studio_analytics(
        self,
    ) -> None:
        """
        Open Studio analytics.
        """
        ...

    @abstractmethod
    def studio_comments(
        self,
    ) -> None:
        """
        Open Studio comments.
        """
        ...

    @abstractmethod
    def studio_copyright(
        self,
    ) -> None:
        """
        Open Studio copyright.
        """
        ...

    @abstractmethod
    def studio_monetization(
        self,
    ) -> None:
        """
        Open Studio monetization.
        """
        ...

    @abstractmethod
    def studio_settings(
        self,
    ) -> None:
        """
        Open Studio settings.
        """
        ...