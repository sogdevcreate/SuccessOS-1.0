from abc import ABC, abstractmethod
from studio.pipeline.stage_result import StageResult
from studio.models.studio_project import StudioProject
class ScenePlanner(ABC):
    @abstractmethod
    def plan(self, project: StudioProject) -> StageResult: ...
