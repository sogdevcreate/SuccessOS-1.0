from dataclasses import dataclass


@dataclass
class Video:
    identifier: str
    location: str | None = None
    duration_seconds: float = 0.0
    thumbnail_location: str | None = None

    def to_dict(self) -> dict[str, object]:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Video":
        return cls(**data)
