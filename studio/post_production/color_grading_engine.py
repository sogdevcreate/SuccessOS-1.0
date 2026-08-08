from studio.enums import PipelineStage,StageStatus
from studio.pipeline.stage_result import StageResult
class ColorGradingEngine:
    def __init__(self,reviewer):self.reviewer=reviewer
    def grade(self,project):
        if project.stage_statuses.get(PipelineStage.VIDEO_EDIT) is not StageStatus.SUCCEEDED:
            return StageResult.failed(PipelineStage.COLOR_GRADING,"Color grading cannot begin until Video Editing is approved")
        if project.edit_project is None:return StageResult.failed(PipelineStage.COLOR_GRADING,"Color grading requires an approved EditProject")
        if project.color_grade is None:return StageResult.failed(PipelineStage.COLOR_GRADING,"Color grading requires a populated ColorGrade")
        return StageResult(PipelineStage.COLOR_GRADING,StageStatus.SUCCEEDED,quality_report=self.reviewer.review(project.color_grade,project))
