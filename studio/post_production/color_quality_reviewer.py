from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore
from studio.enums import PipelineStage
class ColorQualityReviewer:
    CRITERIA=("shot_matching","skin_tone_realism","exposure_consistency","white_balance_consistency","palette_consistency","cinematic_quality","lighting_continuity","scene_continuity","production_profile_compliance","directors_bible_compliance")
    def review(self,grade,project):
        profile=project.production_profile;bible=project.directors_bible
        valid=bool(grade.shot_grades and grade.profile.look_profile and profile.realism_level and bible.visual_rules and all(shot.saturation.skin_tone_protection for shot in grade.shot_grades))
        score=10. if valid else 0.;report=QualityReport(PipelineStage.VIDEO_EDIT,[QualityScore(item,score) for item in self.CRITERIA],project.production_settings.quality_threshold);report.evaluate();return report
