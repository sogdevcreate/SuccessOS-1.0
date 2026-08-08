from dataclasses import dataclass
from studio.scene_planning.asset_specification import AssetSpecification
@dataclass
class VFXAssetSpec:
    specification: AssetSpecification
    effects: list[str]
    def to_dict(self): return {"specification": self.specification.to_dict(), "effects": list(self.effects)}
    @classmethod
    def from_dict(cls, data): return cls(AssetSpecification.from_dict(data["specification"]), list(data.get("effects", [])))
