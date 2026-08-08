from studio.enums import PipelineStage
from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore
from studio.screenwriting.screenplay import Screenplay
from studio.storyboard.storyboard import CinematicStoryboard


class StoryboardQualityReviewer:
    CRITERIA = ("cinematic_composition", "shot_variety", "shot_motivation", "camera_continuity", "lighting_consistency", "visual_storytelling", "emotional_impact", "pacing", "character_continuity", "environment_continuity", "screenplay_fidelity", "production_profile_compliance", "directors_bible_compliance", "photorealistic_production_feasibility")

    def review(self, storyboard: CinematicStoryboard, screenplay: Screenplay, profile, bible, threshold: float, maximum_retry_count: int = 2, regeneration_count: int = 0) -> QualityReport:
        scores = [QualityScore(criterion, self._score(criterion, storyboard, screenplay, profile, bible)) for criterion in self.CRITERIA]
        report = QualityReport(PipelineStage.STORYBOARD, scores, threshold, maximum_retry_count=maximum_retry_count, regeneration_count=regeneration_count)
        report.evaluate()
        return report

    def _score(self, criterion: str, storyboard: CinematicStoryboard, screenplay: Screenplay, profile, bible) -> float:
        shots = storyboard.shots
        if criterion == "cinematic_composition": return 10.0 * sum(bool(shot.composition.framing and shot.composition.camera_angle) for shot in shots) / len(shots) if shots else 0.0
        if criterion == "shot_variety": return min(10.0, len({shot.shot_type for shot in shots}) * 2.5)
        if criterion == "shot_motivation": return 10.0 * sum(bool(shot.camera_plan.target) for shot in shots) / len(shots) if shots else 0.0
        if criterion == "camera_continuity": return 10.0 if all(shot.continuity.axis_of_action for shot in shots) else 0.0
        if criterion == "lighting_consistency": return 10.0 * sum(bool(shot.lighting_plan.mood) for shot in shots) / len(shots) if shots else 0.0
        if criterion == "visual_storytelling": return 10.0 * sum(bool(scene.visual_summary) for scene in storyboard.scenes) / len(storyboard.scenes) if storyboard.scenes else 0.0
        if criterion == "emotional_impact": return 10.0 * sum(bool(shot.composition.mood) for shot in shots) / len(shots) if shots else 0.0
        if criterion == "pacing": return 10.0 if storyboard.estimated_runtime_seconds > 0 else 0.0
        if criterion == "character_continuity": return 10.0 * sum(bool(shot.continuity.character_requirements) for shot in shots) / len(shots) if shots else 0.0
        if criterion == "environment_continuity": return 10.0 * sum(bool(shot.environment_requirements and shot.continuity.location_requirements) for shot in shots) / len(shots) if shots else 0.0
        if criterion == "screenplay_fidelity": return 10.0 * sum(shot.scene_id in {scene.id for scene in screenplay.scenes} for shot in shots) / len(shots) if shots else 0.0
        if criterion == "production_profile_compliance": return 10.0 if profile.visual_style and profile.realism_level else 0.0
        if criterion == "directors_bible_compliance": return 10.0 if bible.visual_rules and all(shot.continuity.lighting_requirements for shot in shots) else 0.0
        return 10.0 if storyboard.visual_style_target.casefold() == "cinematic photorealism" else 0.0
