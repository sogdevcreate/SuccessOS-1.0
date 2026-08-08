from dataclasses import dataclass


@dataclass
class VoiceIdentity:
    reference: str = ""
    tone: str = ""
    cadence: str = ""

    def to_dict(self) -> dict[str, object]: return self.__dict__.copy()
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "VoiceIdentity": return cls(**data)
