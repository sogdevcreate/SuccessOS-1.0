from copy import deepcopy
from uuid import uuid4

from studio.models.project_version import ProjectVersion
from studio.models.studio_project import StudioProject
from studio.services.project_repository import ProjectRepository


class VersionManager:
    def __init__(self, repository: ProjectRepository) -> None:
        self._repository = repository

    def create_snapshot(self, project: StudioProject, label: str = "") -> ProjectVersion:
        version = ProjectVersion(identifier=str(uuid4()), sequence=len(project.version_history) + 1, stage=project.current_pipeline_stage, label=label, snapshot=deepcopy(project.to_dict(include_versions=False)))
        project.version_history.append(version)
        self._repository.save(project)
        return version

    def list_versions(self, project: StudioProject) -> list[ProjectVersion]:
        return list(project.version_history)

    def compare_versions(self, first: ProjectVersion, second: ProjectVersion) -> dict[str, dict[str, object]]:
        changes: dict[str, dict[str, object]] = {}
        keys = set(first.snapshot) | set(second.snapshot)
        for key in sorted(keys):
            if first.snapshot.get(key) != second.snapshot.get(key):
                changes[key] = {"before": first.snapshot.get(key), "after": second.snapshot.get(key)}
        return changes

    def restore_version(self, project: StudioProject, version_id: str) -> StudioProject:
        version = next((item for item in project.version_history if item.identifier == version_id), None)
        if version is None:
            raise KeyError(f"Unknown project version: {version_id}")
        restored = StudioProject.from_dict(deepcopy(version.snapshot))
        restored.version_history = list(project.version_history)
        self._repository.save(restored)
        return restored

    def rollback(self, project: StudioProject) -> StudioProject:
        if not project.version_history:
            raise ValueError("Cannot roll back a project with no versions")
        return self.restore_version(project, project.version_history[-1].identifier)
