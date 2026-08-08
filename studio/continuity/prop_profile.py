from dataclasses import dataclass, field


@dataclass
class PropProfile:
    identity: str
    appearance: str = ""
    dimensions: str = ""
    material: str = ""
    ownership: str = ""
    current_location: str = ""
    scene_usage: list[str] = field(default_factory=list)
    damage_state: str = ""
    continuity_history: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]: return {"identity": self.identity, "appearance": self.appearance, "dimensions": self.dimensions, "material": self.material, "ownership": self.ownership, "current_location": self.current_location, "scene_usage": list(self.scene_usage), "damage_state": self.damage_state, "continuity_history": list(self.continuity_history)}
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "PropProfile": return cls(**data)
