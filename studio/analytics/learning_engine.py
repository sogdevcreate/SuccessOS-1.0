from studio.enums import PipelineStage
from studio.pipeline.stage_result import StageResult
class LearningEngine:
    def __init__(self, validator): self._validator=validator
    def __call__(self, context):
        if not context.project.analytics_reports: return StageResult.failed(PipelineStage.LEARNING,"Learning requires analytics reports")
        return StageResult.failed(PipelineStage.LEARNING,"No learning analysis has been submitted for review")
