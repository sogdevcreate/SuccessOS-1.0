from dataclasses import dataclass, field

from studio.storyboard.lens_profile import LensProfile


@dataclass
class CameraPlan:
    position: str
    target: str
    movement_path: str = ""
    lens_profile: LensProfile | None = None
    stabilization_style: str = ""
    speed: str = ""
    timing: str = ""
    focus_transitions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {"position": self.position, "target": self.target, "movement_path": self.movement_path, "lens_profile": self.lens_profile.to_dict() if self.lens_profile else None, "stabilization_style": self.stabilization_style, "speed": self.speed, "timing": self.timing, "focus_transitions": list(self.focus_transitions)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "CameraPlan":
        values = dict(data)
        values["lens_profile"] = LensProfile.from_dict(values["lens_profile"]) if values.get("lens_profile") else None
        return cls(**values)
