from dataclasses import dataclass


@dataclass
class FacialProfile:
    face_shape: str = ""
    jaw: str = ""
    nose: str = ""
    eyes: str = ""
    eyebrows: str = ""
    lips: str = ""
    skin_texture: str = ""
    complexion: str = ""
    facial_hair: str = ""
    hairstyle: str = ""
    age_appearance: str = ""
    distinctive_marks: list[str] | None = None

    def to_dict(self) -> dict[str, object]:
        data = self.__dict__.copy(); data["distinctive_marks"] = list(self.distinctive_marks or []); return data

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "FacialProfile": return cls(**data)
