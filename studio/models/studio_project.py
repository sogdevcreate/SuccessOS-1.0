from dataclasses import dataclass, field
from uuid import uuid4

from studio.enums import PipelineStage, ProjectStatus, StageStatus
from studio.models.analytics import Analytics
from studio.models.animation import Animation
from studio.models.asset import Asset
from studio.models.audio import Audio
from studio.models.character import Character
from studio.models.production_settings import ProductionSettings
from studio.models.project_metadata import ProjectMetadata
from studio.models.project_version import ProjectVersion
from studio.models.publishing import PublishingMetadata
from studio.models.quality_report import QualityReport
from studio.models.research import Research
from studio.models.scene import Scene
from studio.models.script import Script
from studio.models.storyboard import Storyboard
from studio.models.video import Video


@dataclass
class StudioProject:
    metadata: ProjectMetadata
    identifier: str = field(default_factory=lambda: str(uuid4()))
    production_settings: ProductionSettings = field(default_factory=ProductionSettings)
    research: Research | None = None
    script: Script | None = None
    storyboard: Storyboard | None = None
    characters: list[Character] = field(default_factory=list)
    scenes: list[Scene] = field(default_factory=list)
    assets: list[Asset] = field(default_factory=list)
    animations: list[Animation] = field(default_factory=list)
    audio: list[Audio] = field(default_factory=list)
    video: Video | None = None
    publishing_metadata: PublishingMetadata = field(default_factory=PublishingMetadata)
    analytics: Analytics = field(default_factory=Analytics)
    quality_reports: list[QualityReport] = field(default_factory=list)
    version_history: list[ProjectVersion] = field(default_factory=list)
    current_pipeline_stage: PipelineStage = PipelineStage.IDEA
    status: ProjectStatus = ProjectStatus.DRAFT
    stage_statuses: dict[PipelineStage, StageStatus] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.stage_statuses:
            self.stage_statuses = {stage: StageStatus.PENDING for stage in PipelineStage}

    def to_dict(self, include_versions: bool = True) -> dict[str, object]:
        data: dict[str, object] = {
            "identifier": self.identifier, "metadata": self.metadata.to_dict(), "production_settings": self.production_settings.to_dict(),
            "research": self.research.to_dict() if self.research else None, "script": self.script.to_dict() if self.script else None,
            "storyboard": self.storyboard.to_dict() if self.storyboard else None, "characters": [item.to_dict() for item in self.characters],
            "scenes": [item.to_dict() for item in self.scenes], "assets": [item.to_dict() for item in self.assets],
            "animations": [item.to_dict() for item in self.animations], "audio": [item.to_dict() for item in self.audio],
            "video": self.video.to_dict() if self.video else None, "publishing_metadata": self.publishing_metadata.to_dict(),
            "analytics": self.analytics.to_dict(), "quality_reports": [item.to_dict() for item in self.quality_reports],
            "current_pipeline_stage": self.current_pipeline_stage.value, "status": self.status.value,
            "stage_statuses": {stage.value: value.value for stage, value in self.stage_statuses.items()},
        }
        if include_versions:
            data["version_history"] = [item.to_dict(include_snapshot=False) for item in self.version_history]
        return data

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "StudioProject":
        optional = lambda key, model: model.from_dict(data[key]) if data.get(key) else None
        project = cls(identifier=str(data["identifier"]), metadata=ProjectMetadata.from_dict(data["metadata"]), production_settings=ProductionSettings.from_dict(data.get("production_settings", {})), research=optional("research", Research), script=optional("script", Script), storyboard=optional("storyboard", Storyboard), characters=[Character.from_dict(item) for item in data.get("characters", [])], scenes=[Scene.from_dict(item) for item in data.get("scenes", [])], assets=[Asset.from_dict(item) for item in data.get("assets", [])], animations=[Animation.from_dict(item) for item in data.get("animations", [])], audio=[Audio.from_dict(item) for item in data.get("audio", [])], video=optional("video", Video), publishing_metadata=PublishingMetadata.from_dict(data.get("publishing_metadata", {})), analytics=Analytics.from_dict(data.get("analytics", {})), quality_reports=[QualityReport.from_dict(item) for item in data.get("quality_reports", [])], version_history=[ProjectVersion.from_dict(item) for item in data.get("version_history", [])], current_pipeline_stage=PipelineStage(str(data.get("current_pipeline_stage", PipelineStage.IDEA.value))), status=ProjectStatus(str(data.get("status", ProjectStatus.DRAFT.value))), stage_statuses={PipelineStage(key): StageStatus(value) for key, value in data.get("stage_statuses", {}).items()})
        return project
