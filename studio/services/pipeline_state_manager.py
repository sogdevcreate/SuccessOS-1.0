from studio.enums import PipelineStage, ProjectStatus, StageStatus
from studio.models.studio_project import StudioProject


class PipelineStateManager:
    def mark_stage(self, project: StudioProject, stage: PipelineStage, status: StageStatus) -> None:
        project.stage_statuses[stage] = status
        project.current_pipeline_stage = stage

    def pause(self, project: StudioProject) -> None:
        project.status = ProjectStatus.PAUSED
        self.mark_stage(project, project.current_pipeline_stage, StageStatus.PAUSED)

    def resume(self, project: StudioProject) -> None:
        if project.status is ProjectStatus.PAUSED:
            project.status = ProjectStatus.ACTIVE
            self.mark_stage(project, project.current_pipeline_stage, StageStatus.PENDING)

    def cancel(self, project: StudioProject) -> None:
        project.status = ProjectStatus.CANCELLED
        self.mark_stage(project, project.current_pipeline_stage, StageStatus.CANCELLED)
