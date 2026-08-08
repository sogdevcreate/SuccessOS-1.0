from dataclasses import dataclass, field
from datetime import datetime

from studio.models import deserialize_datetime, serialize, utc_now


@dataclass
class ProjectMetadata:
    title: str
    creator: str
    description: str = ""
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, object]:
        return serialize(self)

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ProjectMetadata":
        return cls(**{**data, "created_at": deserialize_datetime(data.get("created_at")), "updated_at": deserialize_datetime(data.get("updated_at"))})
