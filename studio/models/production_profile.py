from dataclasses import dataclass


@dataclass
class ProductionProfile:
    """Creative and delivery constraints shared by every production stage."""

    target_platform: str = ""
    genre: str = ""
    realism_level: str = ""
    visual_style: str = ""
    rendering_quality: str = ""
    camera_style: str = ""
    lighting_style: str = ""
    color_profile: str = ""
    motion_style: str = ""
    voice_style: str = ""
    music_style: str = ""
    audience: str = ""
    duration: int = 0
    language: str = "en"

    def __post_init__(self) -> None:
        if self.duration < 0:
            raise ValueError("duration cannot be negative")

    def to_dict(self) -> dict[str, object]:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ProductionProfile":
        return cls(**data)
