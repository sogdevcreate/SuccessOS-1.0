from dataclasses import dataclass


@dataclass
class ExposureAdjustment:
    stops: float = 0.0
    highlights: float = 0.0
    shadows: float = 0.0
    black_level: float = 0.0

    def to_dict(self) -> dict[str, float]: return self.__dict__.copy()
    @classmethod
    def from_dict(cls, data: dict[str, float]) -> "ExposureAdjustment": return cls(**data)
