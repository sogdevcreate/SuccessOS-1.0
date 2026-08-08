"""Serializable Studio domain models."""

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def serialize(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if is_dataclass(value):
        return serialize(asdict(value))
    if isinstance(value, dict):
        return {str(key): serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    return value


def deserialize_datetime(value: str | datetime | None) -> datetime | None:
    if value is None or isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


from studio.models.analytics import Analytics
from studio.models.animation import Animation
from studio.models.asset import Asset
from studio.models.audio import Audio
from studio.models.character import Character
from studio.models.directors_bible import DirectorsBible
from studio.models.production_settings import ProductionSettings
from studio.models.production_profile import ProductionProfile
from studio.models.project_metadata import ProjectMetadata
from studio.models.project_version import ProjectVersion
from studio.models.publishing import PublishingMetadata
from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore
from studio.models.research import Research
from studio.models.scene import Scene
from studio.models.script import Script
from studio.models.storyboard import Storyboard, StoryboardFrame
from studio.models.video import Video
from studio.models.studio_project import StudioProject
from studio.screenwriting.screenplay import Screenplay

__all__ = [
    "Analytics", "Animation", "Asset", "Audio", "Character", "DirectorsBible", "ProductionProfile", "ProductionSettings",
    "ProjectMetadata", "ProjectVersion", "PublishingMetadata", "QualityReport",
    "QualityScore", "Research", "Scene", "Script", "Storyboard", "StoryboardFrame",
    "Screenplay", "StudioProject", "Video", "deserialize_datetime", "serialize", "utc_now",
]
