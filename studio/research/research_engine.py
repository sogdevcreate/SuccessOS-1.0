from abc import ABC, abstractmethod

from studio.enums import PipelineStage, StageStatus
from studio.pipeline.pipeline_context import PipelineContext
from studio.pipeline.stage_result import StageResult
from studio.research.research_pipeline import ResearchPipeline
from studio.research.research_quality_reviewer import ResearchQualityReviewer
from studio.research.research_source import ResearchSource


class ResearchSourceProvider(ABC):
    """Future acquisition boundary. Implementations supply sources, never analysis results."""

    @abstractmethod
    def acquire(self, topic: str) -> list[ResearchSource]: ...


class ResearchEngine:
    """Pipeline adapter that validates and reviews a preassembled research report."""

    def __init__(self, research_pipeline: ResearchPipeline, quality_reviewer: ResearchQualityReviewer) -> None:
        self._research_pipeline = research_pipeline
        self._quality_reviewer = quality_reviewer

    def __call__(self, context: PipelineContext) -> StageResult:
        return self.research(context)

    def research(self, context: PipelineContext) -> StageResult:
        project = context.project
        if project.research_report is None:
            return StageResult.failed(PipelineStage.RESEARCH, "Research stage requires a populated ResearchReport")
        try:
            report = self._research_pipeline.analyze(project.research_report)
        except ValueError as error:
            return StageResult.failed(PipelineStage.RESEARCH, str(error))
        project.research_report = report
        quality_report = self._quality_reviewer.review(report, threshold=project.production_settings.quality_threshold, maximum_retry_count=project.production_settings.maximum_regeneration_count)
        return StageResult(stage=PipelineStage.RESEARCH, status=StageStatus.SUCCEEDED, quality_report=quality_report)
