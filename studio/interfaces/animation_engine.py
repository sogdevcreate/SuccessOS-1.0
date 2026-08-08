from abc import ABC, abstractmethod
from studio.pipeline.stage_result import StageResult
from studio.models.studio_project import StudioProject
class AnimationEngine(ABC):
    @abstractmethod
    def animate(self, project: StudioProject) -> StageResult: ...
