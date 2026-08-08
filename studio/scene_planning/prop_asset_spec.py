from dataclasses import dataclass
from studio.scene_planning.asset_specification import AssetSpecification
@dataclass
class PropAssetSpec:
    specification: AssetSpecification
    prop_id: str
    ownership: str
    current_location: str
    damage_state: str
    scene_usage: list[str]
    def to_dict(self): return {"specification": self.specification.to_dict(), "prop_id": self.prop_id, "ownership": self.ownership, "current_location": self.current_location, "damage_state": self.damage_state, "scene_usage": list(self.scene_usage)}
    @classmethod
    def from_dict(cls, data): return cls(AssetSpecification.from_dict(data["specification"]), str(data["prop_id"]), str(data["ownership"]), str(data["current_location"]), str(data["damage_state"]), list(data.get("scene_usage", [])))
