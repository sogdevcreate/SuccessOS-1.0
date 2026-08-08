from dataclasses import dataclass, field
from datetime import datetime

from studio.enums import PipelineStage
from studio.models import deserialize_datetime, utc_now


@dataclass
class ProjectVersion:
    identifier: str
    sequence: int
    created_at: datetime = field(default_factory=utc_now)
    stage: PipelineStage | None = None
    label: str = ""
    snapshot: dict[str, object] = field(default_factory=dict, repr=False)

    def to_dict(self, include_snapshot: bool = True) -> dict[str, object]:
        data: dict[str, object] = {"identifier": self.identifier, "sequence": self.sequence, "created_at": self.created_at.isoformat(), "stage": self.stage.value if self.stage else None, "label": self.label}
        if include_snapshot:
            data["snapshot"] = self.snapshot
        return data

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ProjectVersion":
        stage = data.get("stage")
        return cls(identifier=str(data["identifier"]), sequence=int(data["sequence"]), created_at=deserialize_datetime(data.get("created_at")) or utc_now(), stage=PipelineStage(str(stage)) if stage else None, label=str(data.get("label", "")), snapshot=dict(data.get("snapshot", {})))
