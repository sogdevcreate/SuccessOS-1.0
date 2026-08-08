from abc import ABC, abstractmethod

from studio.enums import PipelineStage, StageStatus
from studio.pipeline.pipeline_context import PipelineContext
from studio.pipeline.stage_result import StageResult
from studio.research.research_report import ResearchReport
from studio.screenwriting.screenplay import Screenplay
from studio.screenwriting.screenplay_pipeline import ScreenplayPipeline
from studio.screenwriting.screenplay_quality_reviewer import ScreenplayQualityReviewer


class ScreenplayProvider(ABC):
    """Future LLM boundary. Providers return a typed screenplay, never a stage success flag."""

    @abstractmethod
    def create(self, research_report: ResearchReport, profile, bible) -> Screenplay: ...


class ScreenplayEngine:
    def __init__(self, screenplay_pipeline: ScreenplayPipeline, quality_reviewer: ScreenplayQualityReviewer) -> None:
        self._screenplay_pipeline = screenplay_pipeline
        self._quality_reviewer = quality_reviewer

    def __call__(self, context: PipelineContext) -> StageResult:
        project = context.project
        if project.research_report is None:
            return StageResult.failed(PipelineStage.SCRIPT, "Screenplay stage requires a ResearchReport")
        if project.screenplay is None:
            return StageResult.failed(PipelineStage.SCRIPT, "Screenplay stage requires a populated Screenplay")
        try:
            screenplay = self._screenplay_pipeline.analyze(project.screenplay, project.research_report)
        except ValueError as error:
            return StageResult.failed(PipelineStage.SCRIPT, str(error))
        project.screenplay = screenplay
        quality_report = self._quality_reviewer.review(screenplay, project.research_report, context.production_profile, context.directors_bible, project.production_settings.quality_threshold, project.production_settings.maximum_regeneration_count)
        return StageResult(PipelineStage.SCRIPT, StageStatus.SUCCEEDED, quality_report=quality_report)
