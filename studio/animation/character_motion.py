from dataclasses import dataclass, field


@dataclass
class CharacterMotion:
    character_id: str
    pose_transitions: list[str] = field(default_factory=list)
    gestures: list[str] = field(default_factory=list)
    gait: str = ""

    def to_dict(self) -> dict[str, object]:
        return {"character_id": self.character_id, "pose_transitions": list(self.pose_transitions), "gestures": list(self.gestures), "gait": self.gait}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "CharacterMotion":
        return cls(**data)
