from studio.enums import PipelineStage, StageStatus
from studio.pipeline.pipeline_context import PipelineContext
from studio.pipeline.stage_result import StageResult
from studio.scene_planning.scene_quality_reviewer import SceneQualityReviewer
from studio.scene_planning.scene_validator import SceneValidator
class ScenePlanningEngine:
    def __init__(self, validator: SceneValidator, quality_reviewer: SceneQualityReviewer): self._validator = validator; self._quality_reviewer = quality_reviewer
    def __call__(self, context: PipelineContext) -> StageResult:
        project = context.project
        if project.screenplay is None or project.cinematic_storyboard is None or project.continuity_registry is None: return StageResult.failed(PipelineStage.SCENE_PLANNING, "Scene Planning requires approved screenplay, storyboard, and continuity state")
        if not project.scene_plans or not project.asset_specifications: return StageResult.failed(PipelineStage.SCENE_PLANNING, "Scene Planning requires populated ScenePlans and AssetSpecifications")
        errors = self._validator.validate(project.scene_plans, project.asset_specifications, project)
        if errors: return StageResult.failed(PipelineStage.SCENE_PLANNING, "; ".join(errors))
        return StageResult(PipelineStage.SCENE_PLANNING, StageStatus.SUCCEEDED, quality_report=self._quality_reviewer.review(project.scene_plans, project.asset_specifications, project))
