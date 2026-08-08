from dataclasses import dataclass, field


@dataclass
class Scene:
    identifier: str
    sequence: int
    description: str
    duration_seconds: float = 0.0
    asset_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {"identifier": self.identifier, "sequence": self.sequence, "description": self.description, "duration_seconds": self.duration_seconds, "asset_ids": list(self.asset_ids)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Scene":
        return cls(**data)
