from abc import ABC, abstractmethod
from studio.models.quality_report import QualityReport
from studio.models.studio_project import StudioProject
class Reviewer(ABC):
    @abstractmethod
    def review(self, project: StudioProject) -> QualityReport: ...
