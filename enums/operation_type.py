"""
Operation Type Enumeration.

Represents the operation an Action requests.
"""

from enum import Enum


class OperationType(str, Enum):
    #
    # Application
    #
    OPEN = "open"
    CLOSE = "close"

    #
    # Installation
    #
    INSTALL = "install"
    UNINSTALL = "uninstall"

    #
    # AI / Search
    #
    QUERY = "query"
    SEARCH = "search"

    #
    # Memory
    #
    SAVE = "save"
    LOAD = "load"
    DELETE = "delete"

    #
    # Filesystem
    #
    READ = "read"
    WRITE = "write"
    LIST = "list"
    COPY = "copy"
    MOVE = "move"
    CREATE_DIRECTORY = "create_directory"

    #
    # Clipboard
    #
    CLEAR = "clear"

    #
    # Process
    #
    LIST_PROCESSES = "list_processes"
    START_PROCESS = "start_process"
    KILL_PROCESS = "kill_process"
    PROCESS_INFO = "process_info"

    #
    # Browser
    #
    OPEN_URL = "open_url"
    OPEN_TAB = "open_tab"
    CLOSE_TAB = "close_tab"
    REFRESH_PAGE = "refresh_page"
    GO_BACK = "go_back"
    GO_FORWARD = "go_forward"
    LIST_TABS = "list_tabs"
    CURRENT_TAB = "current_tab"
    SWITCH_TAB = "switch_tab"
    PAGE_TITLE = "page_title"

    #
    # Browser Interaction
    #
    CLICK = "click"
    TYPE = "type"
    PRESS = "press"
    WAIT_FOR = "wait_for"
    SCROLL = "scroll"
    SELECT = "select"
    UPLOAD_FILE = "upload_file"
    SCREENSHOT = "screenshot"

    #
    # YouTube
    #
    YOUTUBE_SEARCH = "youtube_search"
    YOUTUBE_PLAY = "youtube_play"
    YOUTUBE_VIDEO = "youtube_video"
    YOUTUBE_PLAYLIST = "youtube_playlist"
    YOUTUBE_CHANNEL = "youtube_channel"


    #
    # YouTube Studio
    #
    STUDIO_OPEN = "studio_open"
    STUDIO_DASHBOARD = "studio_dashboard"
    STUDIO_CONTENT = "studio_content"
    STUDIO_ANALYTICS = "studio_analytics"
    STUDIO_COMMENTS = "studio_comments"
    STUDIO_COPYRIGHT = "studio_copyright"
    STUDIO_MONETIZATION = "studio_monetization"
    STUDIO_SETTINGS = "studio_settings"

    #
    # System
    #
    SHUTDOWN = "shutdown"
    RESTART = "restart"
    SLEEP = "sleep"
    LOCK = "lock"

    #
    # Chat
    #
    CHAT = "chat"
