from dataclasses import dataclass, field


@dataclass
class StoryboardFrame:
    sequence: int
    description: str
    narration: str = ""
    duration_seconds: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "StoryboardFrame":
        return cls(**data)


@dataclass
class Storyboard:
    frames: list[StoryboardFrame] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {"frames": [frame.to_dict() for frame in self.frames]}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Storyboard":
        return cls(frames=[StoryboardFrame.from_dict(item) for item in data.get("frames", [])])
