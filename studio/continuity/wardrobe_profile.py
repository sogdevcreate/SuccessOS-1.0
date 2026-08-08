from dataclasses import dataclass, field


@dataclass
class WardrobeProfile:
    costume_id: str
    scene_use: list[str] = field(default_factory=list)
    garment_pieces: list[str] = field(default_factory=list)
    colors: list[str] = field(default_factory=list)
    materials: list[str] = field(default_factory=list)
    wear_damage_state: str = ""
    dirt_wetness: str = ""
    accessories: list[str] = field(default_factory=list)
    continuity_transitions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]: return {"costume_id": self.costume_id, "scene_use": list(self.scene_use), "garment_pieces": list(self.garment_pieces), "colors": list(self.colors), "materials": list(self.materials), "wear_damage_state": self.wear_damage_state, "dirt_wetness": self.dirt_wetness, "accessories": list(self.accessories), "continuity_transitions": list(self.continuity_transitions)}
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "WardrobeProfile": return cls(**data)
