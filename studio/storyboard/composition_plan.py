from dataclasses import dataclass


@dataclass
class CompositionPlan:
    framing: str
    camera_angle: str
    camera_height: str
    color_intent: str = ""
    mood: str = ""

    def to_dict(self) -> dict[str, object]:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "CompositionPlan":
        return cls(**data)
