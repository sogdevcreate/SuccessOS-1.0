from abc import ABC, abstractmethod
from studio.pipeline.stage_result import StageResult
from studio.models.studio_project import StudioProject
class CharacterDesigner(ABC):
    @abstractmethod
    def design(self, project: StudioProject) -> StageResult: ...
