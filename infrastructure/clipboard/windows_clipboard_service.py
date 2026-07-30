"""
Windows Clipboard Service.

Windows implementation of ClipboardService.
"""

from __future__ import annotations

import tkinter as tk

from services.clipboard_service import ClipboardService


class WindowsClipboardService(ClipboardService):
    """
    Windows clipboard implementation.
    """

    def get_text(self) -> str:
        root = tk.Tk()
        root.withdraw()

        try:
            return root.clipboard_get()
        except tk.TclError:
            return ""
        finally:
            root.destroy()

    def set_text(
        self,
        text: str,
    ) -> None:
        root = tk.Tk()
        root.withdraw()

        try:
            root.clipboard_clear()
            root.clipboard_append(text)
            root.update()
        finally:
            root.destroy()

    def clear(self) -> None:
        root = tk.Tk()
        root.withdraw()

        try:
            root.clipboard_clear()
            root.update()
        finally:
            root.destroy()