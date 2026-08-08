from dataclasses import dataclass, field
from uuid import uuid4

from studio.enums import PipelineStage, ProjectStatus, StageStatus
from studio.models.analytics import Analytics
from studio.models.animation import Animation
from studio.models.asset import Asset
from studio.models.audio import Audio
from studio.models.character import Character
from studio.models.directors_bible import DirectorsBible
from studio.models.production_profile import ProductionProfile
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
from studio.research.research_report import ResearchReport
from studio.screenwriting.screenplay import Screenplay
from studio.storyboard.storyboard import CinematicStoryboard
from studio.continuity.character_profile import CharacterProfile
from studio.continuity.continuity_registry import ContinuityRegistry
from studio.continuity.environment_profile import EnvironmentProfile
from studio.continuity.prop_profile import PropProfile
from studio.scene_planning.asset_specification import AssetSpecification
from studio.scene_planning.scene_plan import ScenePlan
from studio.generation.generation_request import GenerationRequest
from studio.generation.generated_asset import GeneratedAsset


@dataclass
class StudioProject:
    metadata: ProjectMetadata
    identifier: str = field(default_factory=lambda: str(uuid4()))
    production_settings: ProductionSettings = field(default_factory=ProductionSettings)
    production_profile: ProductionProfile = field(default_factory=ProductionProfile)
    directors_bible: DirectorsBible = field(default_factory=DirectorsBible)
    research: Research | None = None
    research_report: ResearchReport | None = None
    script: Script | None = None
    screenplay: Screenplay | None = None
    cinematic_storyboard: CinematicStoryboard | None = None
    character_profiles: list[CharacterProfile] = field(default_factory=list)
    environment_profiles: list[EnvironmentProfile] = field(default_factory=list)
    prop_profiles: list[PropProfile] = field(default_factory=list)
    continuity_registry: ContinuityRegistry | None = None
    scene_plans: list[ScenePlan] = field(default_factory=list)
    asset_specifications: list[AssetSpecification] = field(default_factory=list)
    generation_requests: list[GenerationRequest] = field(default_factory=list)
    generated_assets: list[GeneratedAsset] = field(default_factory=list)
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
            "production_profile": self.production_profile.to_dict(), "directors_bible": self.directors_bible.to_dict(),
            "research": self.research.to_dict() if self.research else None, "research_report": self.research_report.to_dict() if self.research_report else None, "script": self.script.to_dict() if self.script else None, "screenplay": self.screenplay.to_dict() if self.screenplay else None, "cinematic_storyboard": self.cinematic_storyboard.to_dict() if self.cinematic_storyboard else None, "character_profiles": [item.to_dict() for item in self.character_profiles], "environment_profiles": [item.to_dict() for item in self.environment_profiles], "prop_profiles": [item.to_dict() for item in self.prop_profiles], "continuity_registry": self.continuity_registry.to_dict() if self.continuity_registry else None, "scene_plans": [item.to_dict() for item in self.scene_plans], "asset_specifications": [item.to_dict() for item in self.asset_specifications], "generation_requests": [item.to_dict() for item in self.generation_requests], "generated_assets": [item.to_dict() for item in self.generated_assets],
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
        profile=ProductionProfile.from_dict(data.get("production_profile", {})); bible=DirectorsBible.from_dict(data.get("directors_bible", {})); project = cls(identifier=str(data["identifier"]), metadata=ProjectMetadata.from_dict(data["metadata"]), production_settings=ProductionSettings.from_dict(data.get("production_settings", {})), production_profile=profile, directors_bible=bible, research=optional("research", Research), research_report=optional("research_report", ResearchReport), script=optional("script", Script), screenplay=optional("screenplay", Screenplay), cinematic_storyboard=optional("cinematic_storyboard", CinematicStoryboard), character_profiles=[CharacterProfile.from_dict(item) for item in data.get("character_profiles", [])], environment_profiles=[EnvironmentProfile.from_dict(item) for item in data.get("environment_profiles", [])], prop_profiles=[PropProfile.from_dict(item) for item in data.get("prop_profiles", [])], continuity_registry=optional("continuity_registry", ContinuityRegistry), scene_plans=[ScenePlan.from_dict(item) for item in data.get("scene_plans", [])], asset_specifications=[AssetSpecification.from_dict(item) for item in data.get("asset_specifications", [])], generation_requests=[GenerationRequest.from_dict(item, profile, bible) for item in data.get("generation_requests", [])], generated_assets=[GeneratedAsset.from_dict(item) for item in data.get("generated_assets", [])], storyboard=optional("storyboard", Storyboard), characters=[Character.from_dict(item) for item in data.get("characters", [])], scenes=[Scene.from_dict(item) for item in data.get("scenes", [])], assets=[Asset.from_dict(item) for item in data.get("assets", [])], animations=[Animation.from_dict(item) for item in data.get("animations", [])], audio=[Audio.from_dict(item) for item in data.get("audio", [])], video=optional("video", Video), publishing_metadata=PublishingMetadata.from_dict(data.get("publishing_metadata", {})), analytics=Analytics.from_dict(data.get("analytics", {})), quality_reports=[QualityReport.from_dict(item) for item in data.get("quality_reports", [])], version_history=[ProjectVersion.from_dict(item) for item in data.get("version_history", [])], current_pipeline_stage=PipelineStage(str(data.get("current_pipeline_stage", PipelineStage.IDEA.value))), status=ProjectStatus(str(data.get("status", ProjectStatus.DRAFT.value))), stage_statuses={PipelineStage(key): StageStatus(value) for key, value in data.get("stage_statuses", {}).items()})
        return project
