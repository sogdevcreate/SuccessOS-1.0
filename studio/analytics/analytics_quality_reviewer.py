from studio.enums import PipelineStage
from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore
class AnalyticsQualityReviewer:
    criteria=("completeness","metric_validity","provenance","sample_adequacy","temporal_consistency","cross_source_consistency","privacy_compliance","interpretation_quality")
    def review(self, scores, threshold=7.0): return QualityReport(PipelineStage.ANALYTICS,[QualityScore(name,float(scores.get(name,0)),1.0) for name in self.criteria],threshold)
