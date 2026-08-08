from dataclasses import dataclass


@dataclass
class LocationProfile:
    identity: str
    geography: str = ""
    architecture: str = ""
    time_period: str = ""

    def to_dict(self) -> dict[str, object]: return self.__dict__.copy()
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "LocationProfile": return cls(**data)
