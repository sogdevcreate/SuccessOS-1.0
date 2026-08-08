from dataclasses import dataclass, field


@dataclass
class BlockingPlan:
    subject_positions: list[str] = field(default_factory=list)
    character_blocking: list[str] = field(default_factory=list)
    screen_direction: str = ""
    axis_of_action: str = ""

    def to_dict(self) -> dict[str, object]:
        return {"subject_positions": list(self.subject_positions), "character_blocking": list(self.character_blocking), "screen_direction": self.screen_direction, "axis_of_action": self.axis_of_action}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BlockingPlan":
        return cls(**data)
