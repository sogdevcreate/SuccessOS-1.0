"""Dependency-free fakes for SuccessOS tests."""

from __future__ import annotations

from dataclasses import dataclass, field

from enums.memory_category import MemoryCategory
from models.memory_record import MemoryRecord
from models.system_status import SystemStatus
from models.user_profile import UserProfile


class FakeMemoryService:
    """In-memory memory service used by integration and E2E tests."""

    def __init__(self) -> None:
        self.records: dict[tuple[MemoryCategory, str], MemoryRecord] = {}

    def remember(self, memory: MemoryRecord) -> bool:
        self.records[(memory.category, memory.key)] = memory
        return True

    def recall(
        self,
        category: MemoryCategory,
        key: str,
    ) -> MemoryRecord | None:
        return self.records.get((category, key))

    def forget(self, category: MemoryCategory, key: str) -> bool:
        return self.records.pop((category, key), None) is not None

    def list(self) -> list[MemoryRecord]:
        return list(self.records.values())


class FakeProfileService:
    def __init__(self, profile: UserProfile | None = None) -> None:
        self.profile = profile

    def get_profile(self) -> UserProfile | None:
        return self.profile


class FakeSystemService:
    def get_status(self) -> SystemStatus:
        return SystemStatus(cpu_usage=12.5, memory_usage=50.0)


@dataclass
class FakeBrowserService:
    """Stateful browser fake that verifies workflow outcomes without Selenium."""

    tabs: list[str] = field(default_factory=list)
    active_tab: int = 0
    page_title_value: str = ""
    last_selector: str = ""
    last_text: str = ""
    pressed_keys: list[str] = field(default_factory=list)

    def open_url(self, url: str) -> None:
        if self.tabs:
            self.tabs[self.active_tab] = url
        else:
            self.tabs.append(url)
        self.page_title_value = "Google"

    def open_tab(self, url: str) -> None:
        self.tabs.append(url)
        self.active_tab = len(self.tabs) - 1
        self.page_title_value = url

    def close_tab(self) -> None:
        self.tabs.pop(self.active_tab)
        self.active_tab = max(0, self.active_tab - 1)

    def refresh_page(self) -> None:
        return None

    def go_back(self) -> None:
        return None

    def go_forward(self) -> None:
        return None

    def list_tabs(self) -> list[str]:
        return list(self.tabs)

    def current_tab(self) -> int:
        return self.active_tab

    def switch_tab(self, index: int) -> None:
        self.active_tab = index - 1

    def page_title(self) -> str:
        return self.page_title_value

    def click(self, selector: str) -> None:
        self.last_selector = selector

    def type(self, selector: str, text: str) -> None:
        self.last_selector = selector
        self.last_text = text

    def press(self, key: str) -> None:
        self.pressed_keys.append(key)
        if key.upper() == "ENTER" and self.last_text:
            self.page_title_value = f"{self.last_text} - Google Search"

    def wait_for(self, selector: str, timeout: int = 10) -> None:
        self.last_selector = selector

    def scroll(self, pixels: int) -> None:
        return None

    def select(self, selector: str, value: str) -> None:
        self.last_selector = selector
        self.last_text = value

    def upload_file(self, selector: str, path: str) -> None:
        self.last_selector = selector
        self.last_text = path

    def screenshot(self, path: str) -> None:
        return None
