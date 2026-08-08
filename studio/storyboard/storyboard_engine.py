from abc import ABC, abstractmethod

from studio.enums import PipelineStage, StageStatus
from studio.pipeline.pipeline_context import PipelineContext
from studio.pipeline.stage_result import StageResult
from studio.screenwriting.screenplay import Screenplay
from studio.storyboard.storyboard import CinematicStoryboard
from studio.storyboard.storyboard_pipeline import StoryboardPipeline
from studio.storyboard.storyboard_quality_reviewer import StoryboardQualityReviewer


class StoryboardProvider(ABC):
    """Future visual-planning provider boundary; it cannot render or persist assets."""

    @abstractmethod
    def create(self, screenplay: Screenplay, profile, bible) -> CinematicStoryboard: ...


class StoryboardEngine:
    def __init__(self, storyboard_pipeline: StoryboardPipeline, quality_reviewer: StoryboardQualityReviewer) -> None:
        self._storyboard_pipeline = storyboard_pipeline
        self._quality_reviewer = quality_reviewer

    def __call__(self, context: PipelineContext) -> StageResult:
        project = context.project
        if project.screenplay is None:
            return StageResult.failed(PipelineStage.STORYBOARD, "Storyboard stage requires an approved Screenplay")
        if project.cinematic_storyboard is None:
            return StageResult.failed(PipelineStage.STORYBOARD, "Storyboard stage requires a populated CinematicStoryboard")
        try:
            storyboard = self._storyboard_pipeline.analyze(project.cinematic_storyboard, project.screenplay)
        except ValueError as error:
            return StageResult.failed(PipelineStage.STORYBOARD, str(error))
        project.cinematic_storyboard = storyboard
        quality_report = self._quality_reviewer.review(storyboard, project.screenplay, context.production_profile, context.directors_bible, project.production_settings.quality_threshold, project.production_settings.maximum_regeneration_count)
        return StageResult(PipelineStage.STORYBOARD, StageStatus.SUCCEEDED, quality_report=quality_report)
