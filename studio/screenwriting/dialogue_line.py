from dataclasses import dataclass


@dataclass
class DialogueLine:
    character: str
    text: str
    parenthetical: str = ""

    def to_dict(self) -> dict[str, object]:
        return {"character": self.character, "text": self.text, "parenthetical": self.parenthetical}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "DialogueLine":
        return cls(**data)
