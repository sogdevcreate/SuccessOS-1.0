from studio.models.quality_score import QualityScore
from studio.continuity.continuity_registry import ContinuityRegistry


class EnvironmentQualityReviewer:
    CRITERIA = ("location_consistency", "visual_richness", "cinematic_usability", "photorealistic_feasibility", "continuity_completeness", "directors_bible_compliance", "production_profile_compliance")
    def scores(self, registry: ContinuityRegistry, profile, bible) -> list[QualityScore]:
        environments = list(registry.environments.values())
        return [QualityScore(name, self._score(name, environments, profile, bible)) for name in self.CRITERIA]
    def _score(self, name, environments, profile, bible):
        if not environments: return 0.0
        if name == "location_consistency": return 10.0 * sum(bool(item.identity and item.time_of_day and item.weather) for item in environments) / len(environments)
        if name == "visual_richness": return 10.0 * sum(bool(item.set_profile.materials and item.set_profile.color_palette) for item in environments) / len(environments)
        if name == "cinematic_usability": return 10.0 * sum(bool(item.set_profile.layout and item.lighting_baseline) for item in environments) / len(environments)
        if name == "photorealistic_feasibility": return 10.0 if profile.realism_level else 0.0
        if name == "continuity_completeness": return 10.0 * sum(bool(item.continuity_history) for item in environments) / len(environments)
        if name == "directors_bible_compliance": return 10.0 if bible.visual_rules and bible.lighting_rules else 0.0
        return 10.0 if profile.visual_style else 0.0
