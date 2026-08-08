from dataclasses import dataclass


@dataclass
class ProductionSettings:
    aspect_ratio: str = "16:9"
    target_duration_seconds: int = 300
    language: str = "en"
    quality_threshold: float = 7.0
    maximum_regeneration_count: int = 2

    def __post_init__(self) -> None:
        if not 0.0 <= self.quality_threshold <= 10.0:
            raise ValueError("quality_threshold must be between 0.0 and 10.0")
        if self.maximum_regeneration_count < 0:
            raise ValueError("maximum_regeneration_count cannot be negative")

    def to_dict(self) -> dict[str, object]:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ProductionSettings":
        return cls(**data)
