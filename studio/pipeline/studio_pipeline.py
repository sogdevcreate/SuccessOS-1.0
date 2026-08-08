from collections.abc import Callable

from studio.enums import PipelineStage, ProjectStatus, StageStatus
from studio.models.studio_project import StudioProject
from studio.pipeline.pipeline_context import PipelineContext
from studio.pipeline.stage_result import StageResult
from studio.services.pipeline_state_manager import PipelineStateManager
from studio.services.project_repository import ProjectRepository
from studio.services.quality_manager import QualityManager
from studio.services.version_manager import VersionManager

StageExecutor = Callable[[PipelineContext], StageResult]


class StudioPipeline:
    STAGES = tuple(PipelineStage)
    OPTIONAL_STAGES = frozenset({PipelineStage.CHARACTERS, PipelineStage.ANIMATION, PipelineStage.MUSIC_SFX, PipelineStage.ANALYTICS})

    def __init__(self, repository: ProjectRepository, version_manager: VersionManager, quality_manager: QualityManager, state_manager: PipelineStateManager, executors: dict[PipelineStage, StageExecutor] | None = None) -> None:
        self._repository = repository
        self._version_manager = version_manager
        self._quality_manager = quality_manager
        self._state_manager = state_manager
        self._executors = dict(executors or {})

    def run_stage(self, project: StudioProject, stage: PipelineStage | None = None) -> StageResult:
        target = stage or project.current_pipeline_stage
        if project.status is ProjectStatus.CANCELLED:
            return StageResult.failed(target, "Pipeline is cancelled")
        if project.status is ProjectStatus.PAUSED:
            return StageResult(stage=target, status=StageStatus.PAUSED, message="Pipeline is paused")
        if target is PipelineStage.SCRIPT and project.stage_statuses.get(PipelineStage.RESEARCH) is not StageStatus.SUCCEEDED:
            return StageResult.failed(target, "Script stage requires research that passed its quality gate")
        if target is PipelineStage.STORYBOARD and project.stage_statuses.get(PipelineStage.SCRIPT) is not StageStatus.SUCCEEDED:
            return StageResult.failed(target, "Storyboard stage requires a screenplay that passed its quality gate")
        executor = self._executors.get(target)
        if executor is None:
            self._state_manager.mark_stage(project, target, StageStatus.FAILED)
            project.status = ProjectStatus.FAILED
            self._repository.save(project)
            return StageResult.failed(target, f"No executor is registered for stage '{target.value}'")
        project.status = ProjectStatus.ACTIVE
        self._state_manager.mark_stage(project, target, StageStatus.RUNNING)
        self._repository.save(project)
        result = executor(PipelineContext(project))
        if result.stage is not target:
            result = StageResult.failed(target, "Executor returned a result for a different stage")
        if result.status is not StageStatus.SUCCEEDED:
            self._state_manager.mark_stage(project, target, StageStatus.FAILED if result.status is not StageStatus.SKIPPED else StageStatus.SKIPPED)
            if result.status is not StageStatus.SKIPPED:
                project.status = ProjectStatus.FAILED
            self._repository.save(project)
            return result
        if result.quality_report is not None:
            project.quality_reports.append(result.quality_report)
            if not self._quality_manager.passes(result.quality_report):
                self._state_manager.mark_stage(project, target, StageStatus.FAILED)
                project.status = ProjectStatus.FAILED
                self._repository.save(project)
                return StageResult.failed(target, "Quality gate did not pass")
        self._state_manager.mark_stage(project, target, StageStatus.SUCCEEDED)
        self._version_manager.create_snapshot(project, label=f"Completed {target.value}")
        self._advance(project, target)
        self._repository.save(project)
        return result

    def run(self, project: StudioProject, from_stage: PipelineStage | None = None) -> list[StageResult]:
        start = from_stage or project.current_pipeline_stage
        results: list[StageResult] = []
        for stage in self.STAGES[self.STAGES.index(start):]:
            if project.status in {ProjectStatus.PAUSED, ProjectStatus.CANCELLED, ProjectStatus.FAILED}:
                break
            if project.stage_statuses.get(stage) is StageStatus.SKIPPED:
                continue
            result = self.run_stage(project, stage)
            results.append(result)
            if result.status is not StageStatus.SUCCEEDED:
                break
        return results

    def pause(self, project: StudioProject) -> None:
        self._state_manager.pause(project)
        self._repository.save(project)

    def resume(self, project: StudioProject) -> None:
        self._state_manager.resume(project)
        self._repository.save(project)

    def cancel(self, project: StudioProject) -> None:
        self._state_manager.cancel(project)
        self._repository.save(project)

    def retry_failed_stage(self, project: StudioProject) -> StageResult:
        failed = next((stage for stage in self.STAGES if project.stage_statuses.get(stage) is StageStatus.FAILED), None)
        if failed is None:
            raise ValueError("No failed stage is available to retry")
        project.status = ProjectStatus.ACTIVE
        return self.run_stage(project, failed)

    def skip_optional_stage(self, project: StudioProject, stage: PipelineStage) -> None:
        if stage not in self.OPTIONAL_STAGES:
            raise ValueError(f"Stage '{stage.value}' is not optional")
        if project.stage_statuses.get(stage) is StageStatus.SUCCEEDED:
            raise ValueError("A completed stage cannot be skipped")
        self._state_manager.mark_stage(project, stage, StageStatus.SKIPPED)
        self._repository.save(project)

    def _advance(self, project: StudioProject, stage: PipelineStage) -> None:
        index = self.STAGES.index(stage)
        if index == len(self.STAGES) - 1:
            project.status = ProjectStatus.COMPLETED
        else:
            project.current_pipeline_stage = self.STAGES[index + 1]
