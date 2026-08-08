from dataclasses import dataclass, field
from datetime import date


@dataclass
class TimelineEvent:
    event_date: date
    description: str
    source_references: list[str] = field(default_factory=list)
    confidence: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")

    def to_dict(self) -> dict[str, object]:
        return {"event_date": self.event_date.isoformat(), "description": self.description, "source_references": list(self.source_references), "confidence": self.confidence}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "TimelineEvent":
        return cls(event_date=date.fromisoformat(str(data["event_date"])), description=str(data["description"]), source_references=list(data.get("source_references", [])), confidence=float(data.get("confidence", 0.0)))
