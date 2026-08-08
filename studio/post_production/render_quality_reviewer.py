from studio.enums import PipelineStage
from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore
class RenderQualityReviewer:
 CRITERIA=("image_integrity","frame_integrity","audio_integrity","av_synchronization","subtitle_integrity","color_correctness","resolution_correctness","frame_rate_correctness","artifact_absence","playback_readiness","target_profile_compliance","production_profile_compliance","directors_bible_compliance")
 def review(self,result,project):
  score=10. if result.reference_uri else 0.;report=QualityReport(PipelineStage.RENDERING,[QualityScore(x,score) for x in self.CRITERIA],project.production_settings.quality_threshold);report.evaluate();return report
