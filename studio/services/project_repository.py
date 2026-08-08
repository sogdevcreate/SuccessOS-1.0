from abc import ABC, abstractmethod

from studio.models.studio_project import StudioProject


class ProjectRepository(ABC):
    @abstractmethod
    def save(self, project: StudioProject) -> StudioProject: ...

    @abstractmethod
    def get(self, project_id: str) -> StudioProject | None: ...


class InMemoryProjectRepository(ProjectRepository):
    """A deterministic repository implementation for composition and local testing."""

    def __init__(self) -> None:
        self._projects: dict[str, StudioProject] = {}

    def save(self, project: StudioProject) -> StudioProject:
        self._projects[project.identifier] = project
        return project

    def get(self, project_id: str) -> StudioProject | None:
        return self._projects.get(project_id)
