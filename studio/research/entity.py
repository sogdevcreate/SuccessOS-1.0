from dataclasses import dataclass, field
from enum import Enum


class EntityType(str, Enum):
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    DATE = "date"
    TERM = "term"
    OTHER = "other"


@dataclass
class Entity:
    name: str
    entity_type: EntityType
    source_references: list[str] = field(default_factory=list)
    confidence: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")

    def to_dict(self) -> dict[str, object]:
        return {"name": self.name, "entity_type": self.entity_type.value, "source_references": list(self.source_references), "confidence": self.confidence}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Entity":
        return cls(name=str(data["name"]), entity_type=EntityType(str(data["entity_type"])), source_references=list(data.get("source_references", [])), confidence=float(data.get("confidence", 0.0)))
