from dataclasses import dataclass


@dataclass
class Audio:
    identifier: str
    kind: str
    location: str | None = None
    duration_seconds: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Audio":
        return cls(**data)
