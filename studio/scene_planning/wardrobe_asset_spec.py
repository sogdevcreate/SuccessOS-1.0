from dataclasses import dataclass
from studio.scene_planning.asset_specification import AssetSpecification
@dataclass
class WardrobeAssetSpec:
    specification: AssetSpecification
    costume_id: str
    continuity_state: str
    def to_dict(self): return {"specification": self.specification.to_dict(), "costume_id": self.costume_id, "continuity_state": self.continuity_state}
    @classmethod
    def from_dict(cls, data): return cls(AssetSpecification.from_dict(data["specification"]), str(data["costume_id"]), str(data["continuity_state"]))
