from dataclasses import dataclass
from studio.scene_planning.asset_specification import AssetSpecification
@dataclass
class LightingAssetSpec:
    specification: AssetSpecification
    lighting_intent: str
    def to_dict(self): return {"specification": self.specification.to_dict(), "lighting_intent": self.lighting_intent}
    @classmethod
    def from_dict(cls, data): return cls(AssetSpecification.from_dict(data["specification"]), str(data["lighting_intent"]))
