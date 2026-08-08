from abc import ABC, abstractmethod
from studio.pipeline.stage_result import StageResult
from studio.models.studio_project import StudioProject
class ThumbnailGenerator(ABC):
    @abstractmethod
    def generate(self, project: StudioProject) -> StageResult: ...
