from dataclasses import dataclass, field


@dataclass
class Script:
    title: str
    content: str
    estimated_duration_seconds: int = 0
    sections: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {"title": self.title, "content": self.content, "estimated_duration_seconds": self.estimated_duration_seconds, "sections": list(self.sections)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Script":
        return cls(**data)
