from studio.enums import PipelineStage
from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore
class SceneQualityReviewer:
    CRITERIA = ("completeness", "cinematic_feasibility", "continuity_compliance", "photorealistic_feasibility", "asset_dependency_correctness", "generation_clarity", "provider_readiness", "screenplay_fidelity", "storyboard_fidelity", "directors_bible_compliance", "production_profile_compliance")
    def review(self, plans, specs, project):
        score = lambda name: self._score(name, plans, specs, project)
        report = QualityReport(PipelineStage.SCENE_PLANNING, [QualityScore(name, score(name)) for name in self.CRITERIA], project.production_settings.quality_threshold, maximum_retry_count=project.production_settings.maximum_regeneration_count); report.evaluate(); return report
    def _score(self, name, plans, specs, project):
        if not plans or not specs: return 0.0
        if name == "completeness": return 10.0 * sum(bool(p.location and p.time_of_day and p.required_assets) for p in plans) / len(plans)
        if name == "cinematic_feasibility": return 10.0 * sum(bool(p.camera_shot_references and p.lighting_intent) for p in plans) / len(plans)
        if name == "continuity_compliance": return 10.0 * sum(bool(p.continuity_bindings) for p in plans) / len(plans)
        if name == "photorealistic_feasibility": return 10.0 if project.production_profile.realism_level else 0.0
        if name == "asset_dependency_correctness": return 10.0 * sum(set(s.dependencies).issubset({x.id for x in specs}) for s in specs) / len(specs)
        if name == "generation_clarity": return 10.0 * sum(bool(s.generation_instruction.prompt and s.generation_instruction.negative_prompt) for s in specs) / len(specs)
        if name == "provider_readiness": return 10.0 * sum(bool(s.generation_instruction.modalities and s.resolution and s.aspect_ratio) for s in specs) / len(specs)
        if name == "screenplay_fidelity": return 10.0 * sum(bool(p.screenplay_scene_id) for p in plans) / len(plans)
        if name == "storyboard_fidelity": return 10.0 * sum(bool(p.storyboard_scene_id and p.camera_shot_references) for p in plans) / len(plans)
        if name == "directors_bible_compliance": return 10.0 if project.directors_bible.visual_rules else 0.0
        return 10.0 if project.production_profile.visual_style else 0.0
