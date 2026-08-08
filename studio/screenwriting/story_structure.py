from dataclasses import dataclass, field


@dataclass
class StoryStructure:
    acts: list[str] = field(default_factory=list)
    sequences: list[str] = field(default_factory=list)
    climax: str = ""
    resolution: str = ""

    def to_dict(self) -> dict[str, object]:
        return {"acts": list(self.acts), "sequences": list(self.sequences), "climax": self.climax, "resolution": self.resolution}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "StoryStructure":
        return cls(**data)
