from dataclasses import dataclass

from studio.models.studio_project import StudioProject
from studio.models.production_profile import ProductionProfile
from studio.models.directors_bible import DirectorsBible


@dataclass
class PipelineContext:
    project: StudioProject

    @property
    def production_profile(self) -> ProductionProfile:
        """The immutable-by-convention profile supplied to every stage."""
        return self.project.production_profile

    @property
    def directors_bible(self) -> DirectorsBible:
        """The project-wide creative direction supplied to every stage."""
        return self.project.directors_bible
