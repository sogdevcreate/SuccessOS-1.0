from abc import ABC, abstractmethod
from studio.pipeline.stage_result import StageResult
from studio.models.studio_project import StudioProject
class Publisher(ABC):
    @abstractmethod
    def publish(self, project: StudioProject) -> StageResult: ...
