from studio.enums import PipelineStage
from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore
class AnimationQualityReviewer:
 CRITERIA=("photorealism","motion_naturalness","body_consistency","facial_consistency","lip_sync_accuracy","emotional_performance","identity_preservation","wardrobe_continuity","prop_continuity","environment_continuity","camera_fidelity","lighting_continuity","temporal_stability","artifact_absence","anatomical_correctness","shot_to_shot_continuity","screenplay_fidelity","storyboard_fidelity","directors_bible_compliance","production_profile_compliance")
 def review(self,shot,project):
  score=10. if shot.provenance.get("validated")=="true" else 0.; report=QualityReport(PipelineStage.ANIMATION,[QualityScore(x,score) for x in self.CRITERIA],project.production_settings.quality_threshold);report.evaluate();return report
