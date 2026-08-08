from studio.models.quality_score import QualityScore
from studio.continuity.continuity_registry import ContinuityRegistry


class CharacterQualityReviewer:
    CRITERIA = ("identity_completeness", "photorealistic_feasibility", "visual_consistency", "performance_usefulness", "directors_bible_compliance", "production_profile_compliance")
    def scores(self, registry: ContinuityRegistry, profile, bible) -> list[QualityScore]:
        characters = list(registry.characters.values())
        return [QualityScore(name, self._score(name, characters, profile, bible)) for name in self.CRITERIA]
    def _score(self, name, characters, profile, bible):
        if not characters: return 0.0
        if name == "identity_completeness": return 10.0 * sum(bool(item.identity.name and item.facial_profile.face_shape and item.body_profile.build) for item in characters) / len(characters)
        if name == "photorealistic_feasibility": return 10.0 * sum(bool(item.visual_identity_lock.locked_appearance_attributes) for item in characters) / len(characters)
        if name == "visual_consistency": return 10.0 * sum(bool(item.wardrobe and item.visual_identity_lock.prompt_anchors) for item in characters) / len(characters)
        if name == "performance_usefulness": return 10.0 * sum(bool(item.mannerisms and item.emotional_baseline and item.voice_identity.reference) for item in characters) / len(characters)
        if name == "directors_bible_compliance": return 10.0 if bible.character_rules else 0.0
        return 10.0 if profile.realism_level else 0.0
