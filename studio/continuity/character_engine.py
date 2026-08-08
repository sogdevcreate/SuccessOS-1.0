from studio.enums import PipelineStage, StageStatus
from studio.models.quality_report import QualityReport
from studio.pipeline.pipeline_context import PipelineContext
from studio.pipeline.stage_result import StageResult
from studio.continuity.character_quality_reviewer import CharacterQualityReviewer
from studio.continuity.continuity_validator import ContinuityValidator
from studio.continuity.environment_quality_reviewer import EnvironmentQualityReviewer


class CharacterEnvironmentContinuityEngine:
    def __init__(self, validator: ContinuityValidator, character_reviewer: CharacterQualityReviewer, environment_reviewer: EnvironmentQualityReviewer) -> None:
        self._validator = validator; self._character_reviewer = character_reviewer; self._environment_reviewer = environment_reviewer
    def __call__(self, context: PipelineContext) -> StageResult:
        project = context.project
        if project.cinematic_storyboard is None:
            return StageResult.failed(PipelineStage.CHARACTERS, "Continuity stage requires an approved CinematicStoryboard")
        registry = project.continuity_registry
        if registry is None:
            return StageResult.failed(PipelineStage.CHARACTERS, "Continuity stage requires a populated ContinuityRegistry")
        errors = self._validator.validate(registry)
        if errors: return StageResult.failed(PipelineStage.CHARACTERS, "; ".join(errors))
        scores = self._character_reviewer.scores(registry, context.production_profile, context.directors_bible) + self._environment_reviewer.scores(registry, context.production_profile, context.directors_bible)
        quality = QualityReport(PipelineStage.CHARACTERS, scores, project.production_settings.quality_threshold, maximum_retry_count=project.production_settings.maximum_regeneration_count)
        quality.evaluate()
        return StageResult(PipelineStage.CHARACTERS, StageStatus.SUCCEEDED, quality_report=quality)
