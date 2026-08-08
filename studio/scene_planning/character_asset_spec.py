from dataclasses import dataclass
from studio.scene_planning.asset_specification import AssetSpecification
@dataclass
class CharacterAssetSpec:
    specification: AssetSpecification
    character_id: str
    facial_profile_binding: str
    body_profile_binding: str
    wardrobe_binding: str
    visual_identity_lock_binding: str
    continuity_state: str
    def to_dict(self): return {"specification": self.specification.to_dict(), "character_id": self.character_id, "facial_profile_binding": self.facial_profile_binding, "body_profile_binding": self.body_profile_binding, "wardrobe_binding": self.wardrobe_binding, "visual_identity_lock_binding": self.visual_identity_lock_binding, "continuity_state": self.continuity_state}
    @classmethod
    def from_dict(cls, data): return cls(AssetSpecification.from_dict(data["specification"]), str(data["character_id"]), str(data["facial_profile_binding"]), str(data["body_profile_binding"]), str(data["wardrobe_binding"]), str(data["visual_identity_lock_binding"]), str(data["continuity_state"]))
