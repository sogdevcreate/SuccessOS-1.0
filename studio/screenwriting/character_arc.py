from dataclasses import dataclass, field


@dataclass
class CharacterArc:
    character: str
    starting_state: str
    ending_state: str
    turning_points: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {"character": self.character, "starting_state": self.starting_state, "ending_state": self.ending_state, "turning_points": list(self.turning_points)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "CharacterArc":
        return cls(**data)
