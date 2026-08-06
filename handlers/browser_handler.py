"""
Browser handler.
"""

from __future__ import annotations

from enums.operation_type import OperationType
from interfaces.handler import Handler
from models.action import Action
from models.execution_result import ExecutionResult
from services.browser_service import BrowserService


class BrowserHandler(Handler):
    """
    Handles browser automation actions.
    """

    def __init__(
        self,
        browser_service: BrowserService,
    ) -> None:
        self._browser_service = browser_service

    def execute(
        self,
        action: Action,
    ) -> ExecutionResult:
        """
        Execute a browser action.
        """

        match action.operation:

            #
            # Navigation
            #

            case OperationType.OPEN_URL:

                url = action.parameters.get(
                    "url",
                )

                if not isinstance(
                    url,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'url'."
                    )

                try:

                    self._browser_service.open_url(
                        url,
                    )

                    return ExecutionResult.ok(
                        message="URL opened successfully.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.OPEN_TAB:

                url = action.parameters.get(
                    "url",
                )

                if not isinstance(
                    url,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'url'."
                    )

                try:

                    self._browser_service.open_tab(
                        url,
                    )

                    return ExecutionResult.ok(
                        message="Tab opened successfully.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.CLOSE_TAB:

                try:

                    self._browser_service.close_tab()

                    return ExecutionResult.ok(
                        message="Tab closed successfully.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.REFRESH_PAGE:

                try:

                    self._browser_service.refresh_page()

                    return ExecutionResult.ok(
                        message="Page refreshed successfully.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.GO_BACK:

                try:

                    self._browser_service.go_back()

                    return ExecutionResult.ok(
                        message="Navigated back.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.GO_FORWARD:

                try:

                    self._browser_service.go_forward()

                    return ExecutionResult.ok(
                        message="Navigated forward.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            #
            # Tabs
            #

            case OperationType.LIST_TABS:

                try:

                    tabs = self._browser_service.list_tabs()

                    return ExecutionResult.ok(
                        message="\n".join(
                            f"{i}: {title}"
                            for i, title in enumerate(
                                tabs,
                                start=1,
                            )
                        ),
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.CURRENT_TAB:

                try:

                    index = self._browser_service.current_tab()

                    return ExecutionResult.ok(
                        message=f"Current tab: {index + 1}",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.SWITCH_TAB:

                index = action.parameters.get(
                    "index",
                )

                if not isinstance(
                    index,
                    int,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'index'."
                    )

                try:

                    self._browser_service.switch_tab(
                        index,
                    )

                    return ExecutionResult.ok(
                        message="Switched to tab successfully.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.PAGE_TITLE:

                try:

                    title = self._browser_service.page_title()

                    return ExecutionResult.ok(
                        message=title,
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            #
            # Browser Interaction
            #

            case OperationType.CLICK:

                selector = action.parameters.get(
                    "selector",
                )

                if not isinstance(
                    selector,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'selector'."
                    )

                try:

                    self._browser_service.click(
                        selector,
                    )

                    return ExecutionResult.ok(
                        message="Element clicked successfully.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.TYPE:

                selector = action.parameters.get(
                    "selector",
                )

                text = action.parameters.get(
                    "text",
                )

                if not isinstance(
                    selector,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'selector'."
                    )

                if not isinstance(
                    text,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'text'."
                    )

                try:

                    self._browser_service.type(
                        selector,
                        text,
                    )

                    return ExecutionResult.ok(
                        message="Text entered successfully.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.PRESS:

                key = action.parameters.get(
                    "key",
                )

                if not isinstance(
                    key,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'key'."
                    )

                try:

                    self._browser_service.press(
                        key,
                    )

                    return ExecutionResult.ok(
                        message="Key pressed successfully.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.WAIT_FOR:

                selector = action.parameters.get(
                    "selector",
                )

                timeout = action.parameters.get(
                    "timeout",
                    10,
                )

                if not isinstance(
                    selector,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'selector'."
                    )

                try:

                    self._browser_service.wait_for(
                        selector,
                        timeout,
                    )

                    return ExecutionResult.ok(
                        message="Element appeared.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.SCROLL:

                pixels = action.parameters.get(
                    "pixels",
                )

                if not isinstance(
                    pixels,
                    int,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'pixels'."
                    )

                try:

                    self._browser_service.scroll(
                        pixels,
                    )

                    return ExecutionResult.ok(
                        message="Page scrolled.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.SELECT:

                selector = action.parameters.get(
                    "selector",
                )

                value = action.parameters.get(
                    "value",
                )

                if not isinstance(
                    selector,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'selector'."
                    )

                if not isinstance(
                    value,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'value'."
                    )

                try:

                    self._browser_service.select(
                        selector,
                        value,
                    )

                    return ExecutionResult.ok(
                        message="Option selected.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.UPLOAD_FILE:

                selector = action.parameters.get(
                    "selector",
                )

                path = action.parameters.get(
                    "path",
                )

                if not isinstance(
                    selector,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'selector'."
                    )

                if not isinstance(
                    path,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'path'."
                    )

                try:

                    self._browser_service.upload_file(
                        selector,
                        path,
                    )

                    return ExecutionResult.ok(
                        message="File uploaded.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.SCREENSHOT:

                path = action.parameters.get(
                    "path",
                )

                if not isinstance(
                    path,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'path'."
                    )

                try:

                    self._browser_service.screenshot(
                        path,
                    )

                    return ExecutionResult.ok(
                        message="Screenshot saved.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            #
            # YouTube
            #

            case OperationType.YOUTUBE_SEARCH:

                query = action.parameters.get(
                    "query",
                )

                if not isinstance(
                    query,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'query'."
                    )

                try:

                    self._browser_service.youtube_search(
                        query,
                    )

                    return ExecutionResult.ok(
                        message="YouTube search opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.YOUTUBE_PLAY:

                query = action.parameters.get(
                    "query",
                )

                if not isinstance(
                    query,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'query'."
                    )

                try:

                    self._browser_service.youtube_play(
                        query,
                    )

                    return ExecutionResult.ok(
                        message="Playing YouTube video.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.YOUTUBE_VIDEO:

                video_id = action.parameters.get(
                    "video_id",
                )

                if not isinstance(
                    video_id,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'video_id'."
                    )

                try:

                    self._browser_service.youtube_video(
                        video_id,
                    )

                    return ExecutionResult.ok(
                        message="YouTube video opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.YOUTUBE_PLAYLIST:

                playlist_id = action.parameters.get(
                    "playlist_id",
                )

                if not isinstance(
                    playlist_id,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'playlist_id'."
                    )

                try:

                    self._browser_service.youtube_playlist(
                        playlist_id,
                    )

                    return ExecutionResult.ok(
                        message="YouTube playlist opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            case OperationType.YOUTUBE_CHANNEL:

                channel = action.parameters.get(
                    "channel",
                )

                if not isinstance(
                    channel,
                    str,
                ):
                    return ExecutionResult.fail(
                        "Missing required parameter: 'channel'."
                    )

                try:

                    self._browser_service.youtube_channel(
                        channel,
                    )

                    return ExecutionResult.ok(
                        message="YouTube channel opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(
                        str(ex),
                    )

            #
            # YouTube Studio
            #

            case OperationType.STUDIO_OPEN:

                try:

                    self._browser_service.studio_open()

                    return ExecutionResult.ok(
                        message="YouTube Studio opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(str(ex))

            case OperationType.STUDIO_DASHBOARD:

                try:

                    self._browser_service.studio_dashboard()

                    return ExecutionResult.ok(
                        message="Studio dashboard opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(str(ex))

            case OperationType.STUDIO_CONTENT:

                try:

                    self._browser_service.studio_content()

                    return ExecutionResult.ok(
                        message="Studio content opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(str(ex))

            case OperationType.STUDIO_ANALYTICS:

                try:

                    self._browser_service.studio_analytics()

                    return ExecutionResult.ok(
                        message="Studio analytics opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(str(ex))

            case OperationType.STUDIO_COMMENTS:

                try:

                    self._browser_service.studio_comments()

                    return ExecutionResult.ok(
                        message="Studio comments opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(str(ex))

            case OperationType.STUDIO_COPYRIGHT:

                try:

                    self._browser_service.studio_copyright()

                    return ExecutionResult.ok(
                        message="Studio copyright opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(str(ex))

            case OperationType.STUDIO_MONETIZATION:

                try:

                    self._browser_service.studio_monetization()

                    return ExecutionResult.ok(
                        message="Studio monetization opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(str(ex))

            case OperationType.STUDIO_SETTINGS:

                try:

                    self._browser_service.studio_settings()

                    return ExecutionResult.ok(
                        message="Studio settings opened.",
                    )

                except Exception as ex:

                    return ExecutionResult.fail(str(ex))


            case _:

                return ExecutionResult.fail(
                    f"Unsupported operation: {action.operation.value}"
                )