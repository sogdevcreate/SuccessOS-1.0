from dataclasses import dataclass, field


@dataclass
class ScreenplayBeat:
    sequence: int
    description: str
    emotional_change: str = ""
    tension: float = 0.0
    fact_references: list[str] = field(default_factory=list)
    unsupported_claims: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 0.0 <= self.tension <= 10.0:
            raise ValueError("tension must be between 0.0 and 10.0")

    def to_dict(self) -> dict[str, object]:
        return {"sequence": self.sequence, "description": self.description, "emotional_change": self.emotional_change, "tension": self.tension, "fact_references": list(self.fact_references), "unsupported_claims": list(self.unsupported_claims)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ScreenplayBeat":
        return cls(**data)
