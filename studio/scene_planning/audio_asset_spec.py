from dataclasses import dataclass
from studio.scene_planning.asset_specification import AssetSpecification
@dataclass
class AudioAssetSpec:
    specification: AssetSpecification
    sound_requirements: list[str]
    def to_dict(self): return {"specification": self.specification.to_dict(), "sound_requirements": list(self.sound_requirements)}
    @classmethod
    def from_dict(cls, data): return cls(AssetSpecification.from_dict(data["specification"]), list(data.get("sound_requirements", [])))
