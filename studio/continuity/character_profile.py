from dataclasses import dataclass, field

from studio.continuity.body_profile import BodyProfile
from studio.continuity.character_identity import CharacterIdentity
from studio.continuity.facial_profile import FacialProfile
from studio.continuity.visual_identity_lock import VisualIdentityLock
from studio.continuity.voice_identity import VoiceIdentity
from studio.continuity.wardrobe_profile import WardrobeProfile


@dataclass
class CharacterProfile:
    identity: CharacterIdentity
    facial_profile: FacialProfile = field(default_factory=FacialProfile)
    body_profile: BodyProfile = field(default_factory=BodyProfile)
    mannerisms: list[str] = field(default_factory=list)
    wardrobe: list[WardrobeProfile] = field(default_factory=list)
    accessories: list[str] = field(default_factory=list)
    injuries_scars_marks: list[str] = field(default_factory=list)
    age_progression_state: str = ""
    emotional_baseline: str = ""
    voice_identity: VoiceIdentity = field(default_factory=VoiceIdentity)
    visual_identity_lock: VisualIdentityLock = field(default_factory=VisualIdentityLock)
    continuity_notes: list[str] = field(default_factory=list)

    @property
    def unique_id(self) -> str: return self.identity.unique_id
    @property
    def name(self) -> str: return self.identity.name

    def to_dict(self) -> dict[str, object]:
        return {"identity": self.identity.to_dict(), "facial_profile": self.facial_profile.to_dict(), "body_profile": self.body_profile.to_dict(), "mannerisms": list(self.mannerisms), "wardrobe": [item.to_dict() for item in self.wardrobe], "accessories": list(self.accessories), "injuries_scars_marks": list(self.injuries_scars_marks), "age_progression_state": self.age_progression_state, "emotional_baseline": self.emotional_baseline, "voice_identity": self.voice_identity.to_dict(), "visual_identity_lock": self.visual_identity_lock.to_dict(), "continuity_notes": list(self.continuity_notes)}
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "CharacterProfile":
        return cls(identity=CharacterIdentity.from_dict(data["identity"]), facial_profile=FacialProfile.from_dict(data.get("facial_profile", {})), body_profile=BodyProfile.from_dict(data.get("body_profile", {})), mannerisms=list(data.get("mannerisms", [])), wardrobe=[WardrobeProfile.from_dict(item) for item in data.get("wardrobe", [])], accessories=list(data.get("accessories", [])), injuries_scars_marks=list(data.get("injuries_scars_marks", [])), age_progression_state=str(data.get("age_progression_state", "")), emotional_baseline=str(data.get("emotional_baseline", "")), voice_identity=VoiceIdentity.from_dict(data.get("voice_identity", {})), visual_identity_lock=VisualIdentityLock.from_dict(data.get("visual_identity_lock", {})), continuity_notes=list(data.get("continuity_notes", [])))
