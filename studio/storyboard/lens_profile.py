from dataclasses import dataclass


@dataclass
class LensProfile:
    lens: str
    focal_length_mm: float
    aperture_intent: str = ""
    depth_of_field_intent: str = ""

    def to_dict(self) -> dict[str, object]:
        return {"lens": self.lens, "focal_length_mm": self.focal_length_mm, "aperture_intent": self.aperture_intent, "depth_of_field_intent": self.depth_of_field_intent}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "LensProfile":
        return cls(**data)
