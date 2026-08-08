from studio.enums import PipelineStage
from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore
from studio.research.research_report import ResearchReport
from studio.screenwriting.pacing_analyzer import PacingAnalyzer
from studio.screenwriting.screenplay import Screenplay


class ScreenplayQualityReviewer:
    CRITERIA = ("hook_strength", "storytelling", "structure", "pacing", "emotional_engagement", "dialogue_quality", "narration_quality", "character_consistency", "factual_fidelity", "cinematic_potential", "audience_retention_potential", "production_profile_compliance", "directors_bible_compliance")

    def __init__(self, pacing_analyzer: PacingAnalyzer | None = None) -> None:
        self._pacing_analyzer = pacing_analyzer or PacingAnalyzer()

    def review(self, screenplay: Screenplay, research_report: ResearchReport, profile, bible, threshold: float, maximum_retry_count: int = 2, regeneration_count: int = 0) -> QualityReport:
        scores = [QualityScore(criterion, self._score(criterion, screenplay, research_report, profile, bible)) for criterion in self.CRITERIA]
        report = QualityReport(stage=PipelineStage.SCRIPT, scores=scores, threshold=threshold, maximum_retry_count=maximum_retry_count, regeneration_count=regeneration_count)
        report.evaluate()
        return report

    def _score(self, criterion: str, screenplay: Screenplay, research_report: ResearchReport, profile, bible) -> float:
        scenes = screenplay.scenes
        if criterion == "hook_strength":
            return 10.0 if screenplay.hook else 0.0
        if criterion == "storytelling":
            return 10.0 * sum(bool(item) for item in [screenplay.logline, screenplay.premise, screenplay.opening_sequence, screenplay.climax, screenplay.resolution]) / 5
        if criterion == "structure":
            return min(10.0, len(screenplay.story_structure.acts) * 10.0 / 3)
        if criterion == "pacing":
            curve = self._pacing_analyzer.analyze(screenplay)
            return 10.0 if curve and any(curve) else 0.0
        if criterion == "emotional_engagement":
            return min(10.0, len(screenplay.emotional_arcs) * 5.0)
        if criterion == "dialogue_quality":
            return 10.0 if any(scene.dialogue for scene in scenes) else 0.0
        if criterion == "narration_quality":
            return 10.0 if any(scene.narration for scene in scenes) else 0.0
        if criterion == "character_consistency":
            return 10.0 if screenplay.character_arcs and all(arc.character for arc in screenplay.character_arcs) else 0.0
        if criterion == "factual_fidelity":
            referenced = [scene for scene in scenes if scene.fact_references]
            valid = {fact.identifier for fact in research_report.key_facts}
            return 10.0 * sum(set(scene.fact_references).issubset(valid) and not (set(scene.fact_references).intersection({fact.identifier for fact in research_report.disputed_claims}) - set(scene.disputed_fact_references)) for scene in referenced) / len(referenced) if referenced else 0.0
        if criterion == "cinematic_potential":
            return 10.0 * sum(bool(scene.visual_objective and scene.action_description) for scene in scenes) / len(scenes) if scenes else 0.0
        if criterion == "audience_retention_potential":
            return 10.0 * sum(bool(item) for item in [screenplay.hook, screenplay.reveals, screenplay.callbacks]) / 3
        if criterion == "production_profile_compliance":
            return 10.0 if screenplay.genre == profile.genre and screenplay.target_audience == profile.audience else 0.0
        return 10.0 if scenes and all(scene.directors_bible_constraints for scene in scenes) and bool(bible.story_vision) else 0.0
