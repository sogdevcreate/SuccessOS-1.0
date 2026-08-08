from abc import ABC, abstractmethod
from studio.pipeline.stage_result import StageResult
from studio.models.studio_project import StudioProject
class VideoEditor(ABC):
    @abstractmethod
    def edit(self, project: StudioProject) -> StageResult: ...
