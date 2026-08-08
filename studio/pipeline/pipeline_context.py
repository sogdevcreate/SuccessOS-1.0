from dataclasses import dataclass

from studio.models.studio_project import StudioProject


@dataclass
class PipelineContext:
    project: StudioProject
