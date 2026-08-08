from dataclasses import dataclass


@dataclass
class BodyProfile:
    height: str = ""
    build: str = ""
    proportions: str = ""
    limb_proportions: str = ""
    posture: str = ""
    gait: str = ""
    handedness: str = ""
    movement_characteristics: str = ""

    def to_dict(self) -> dict[str, object]: return self.__dict__.copy()
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BodyProfile": return cls(**data)
