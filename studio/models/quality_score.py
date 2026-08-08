from dataclasses import dataclass


@dataclass(frozen=True)
class QualityScore:
    criterion: str
    score: float
    weight: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 10.0:
            raise ValueError("score must be between 0.0 and 10.0")
        if self.weight < 0.0:
            raise ValueError("weight cannot be negative")

    def to_dict(self) -> dict[str, object]:
        return {"criterion": self.criterion, "score": self.score, "weight": self.weight}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "QualityScore":
        return cls(**data)
