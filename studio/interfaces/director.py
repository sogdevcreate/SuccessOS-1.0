from abc import ABC, abstractmethod
from studio.pipeline.stage_result import StageResult
from studio.models.studio_project import StudioProject
class Director(ABC):
    @abstractmethod
    def approve(self, project: StudioProject) -> StageResult: ...
