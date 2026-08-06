"""YouTube action definitions for the planner prompt."""

from textwrap import dedent


YOUTUBE_PROMPT = dedent(
    """
    ==================================================
    YOUTUBE AND YOUTUBE STUDIO
    ==================================================

    YouTube operations:
    - YOUTUBE_SEARCH {"query": "<search text>"}
    - YOUTUBE_PLAY {"query": "<search text>"}
    - YOUTUBE_VIDEO {"video_id": "<video id>"}
    - YOUTUBE_PLAYLIST {"playlist_id": "<playlist id>"}
    - YOUTUBE_CHANNEL {"channel": "<channel name>"}

    YouTube Studio operations use {}:
    - STUDIO_OPEN
    - STUDIO_DASHBOARD
    - STUDIO_CONTENT
    - STUDIO_ANALYTICS
    - STUDIO_COMMENTS
    - STUDIO_COPYRIGHT
    - STUDIO_MONETIZATION
    - STUDIO_SETTINGS
    """
).strip()
