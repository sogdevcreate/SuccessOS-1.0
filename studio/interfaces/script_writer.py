from abc import ABC, abstractmethod
from studio.pipeline.stage_result import StageResult
from studio.models.studio_project import StudioProject
class ScriptWriter(ABC):
    @abstractmethod
    def write(self, project: StudioProject) -> StageResult: ...
