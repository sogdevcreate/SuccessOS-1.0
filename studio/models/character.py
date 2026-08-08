from dataclasses import dataclass, field


@dataclass
class Character:
    name: str
    description: str
    visual_reference: str | None = None
    traits: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {"name": self.name, "description": self.description, "visual_reference": self.visual_reference, "traits": list(self.traits)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Character":
        return cls(**data)
