from dataclasses import dataclass


@dataclass
class NarrationBlock:
    text: str
    voice: str = ""

    def to_dict(self) -> dict[str, object]:
        return {"text": self.text, "voice": self.voice}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "NarrationBlock":
        return cls(**data)
