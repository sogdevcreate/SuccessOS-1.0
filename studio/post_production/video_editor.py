from studio.enums import PipelineStage,StageStatus
from studio.pipeline.stage_result import StageResult
class VideoEditor:
    def __init__(self,reviewer):self.reviewer=reviewer
    def __call__(self,context):
        p=context.project
        if p.edit_project is None:return StageResult.failed(PipelineStage.VIDEO_EDIT,"Video Edit requires a populated EditProject")
        report=self.reviewer.review(p.edit_project,p)
        return StageResult(PipelineStage.VIDEO_EDIT,StageStatus.SUCCEEDED,quality_report=report)
