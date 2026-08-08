from dataclasses import dataclass, field


@dataclass
class Animation:
    identifier: str
    scene_identifier: str
    location: str | None = None
    settings: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {"identifier": self.identifier, "scene_identifier": self.scene_identifier, "location": self.location, "settings": dict(self.settings)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Animation":
        return cls(**data)
