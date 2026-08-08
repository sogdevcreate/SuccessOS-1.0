from enum import Enum


class PipelineStage(str, Enum):
    IDEA = "idea"
    RESEARCH = "research"
    SCRIPT = "script"
    STORYBOARD = "storyboard"
    CHARACTERS = "characters"
    SCENE_PLANNING = "scene_planning"
    ASSETS = "assets"
    ANIMATION = "animation"
    VOICE = "voice"
    MUSIC_SFX = "music_sfx"
    VIDEO_EDIT = "video_edit"
    COLOR_GRADING = "color_grading"
    RENDERING = "rendering"
    THUMBNAIL = "thumbnail"
    METADATA_SEO = "metadata_seo"
    PUBLISH = "publish"
    ANALYTICS = "analytics"
