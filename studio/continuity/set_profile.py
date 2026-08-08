from dataclasses import dataclass, field


@dataclass
class SetProfile:
    layout: str = ""
    materials: list[str] = field(default_factory=list)
    color_palette: list[str] = field(default_factory=list)
    furniture: list[str] = field(default_factory=list)
    vehicles: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]: return {"layout": self.layout, "materials": list(self.materials), "color_palette": list(self.color_palette), "furniture": list(self.furniture), "vehicles": list(self.vehicles)}
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SetProfile": return cls(**data)
