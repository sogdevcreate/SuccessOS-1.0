from studio.models.quality_score import QualityScore
from studio.models.quality_report import QualityReport
from studio.enums import PipelineStage
class PublishingQualityReviewer:
 CRITERIA=("metadata_completeness","title_quality","description_quality","thumbnail_readiness","chapter_correctness","subtitle_readiness","rights_completeness","disclosure_completeness","platform_compliance","provenance_completeness","production_profile_compliance","directors_bible_compliance")
 def review(self,request,project):
  valid=bool(request.thumbnail_package.selected_candidate and request.rights.resolved and request.provenance and project.production_profile and project.directors_bible)
  s=10. if valid else 0.;r=QualityReport(PipelineStage.PUBLISH,[QualityScore(x,s) for x in self.CRITERIA],project.production_settings.quality_threshold);r.evaluate();return r
