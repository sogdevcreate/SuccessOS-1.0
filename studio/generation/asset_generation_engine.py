from studio.enums import PipelineStage, StageStatus
from studio.generation.generation_request import GenerationRequest
from studio.pipeline.pipeline_context import PipelineContext
from studio.pipeline.stage_result import StageResult
class AssetGenerationEngine:
    def __init__(self, generation_pipeline, quality_reviewer): self._pipeline=generation_pipeline; self._quality_reviewer=quality_reviewer
    def __call__(self, context: PipelineContext):
        project=context.project
        if not project.asset_specifications: return StageResult.failed(PipelineStage.ASSETS,"Asset Generation requires approved AssetSpecifications")
        if not project.generation_requests: return StageResult.failed(PipelineStage.ASSETS,"No provider-ready GenerationRequests are configured")
        try:
            for request in project.generation_requests: self._pipeline.create_job(request)
        except (ValueError,RuntimeError) as error: return StageResult.failed(PipelineStage.ASSETS,str(error))
        if not project.generated_assets: return StageResult.failed(PipelineStage.ASSETS,"Generation jobs are queued; no generated assets are available for acceptance")
        reports=[self._quality_reviewer.review(asset,project) for asset in project.generated_assets]
        if not all(report.passed for report in reports): return StageResult.failed(PipelineStage.ASSETS,"Generated assets did not meet the quality threshold")
        for asset, report in zip(project.generated_assets,reports): asset.quality_report=report; asset.accepted=True
        return StageResult(PipelineStage.ASSETS,StageStatus.SUCCEEDED,quality_report=reports[0])
