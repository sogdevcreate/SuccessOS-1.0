from studio.enums import QualityStatus
from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore


class QualityManager:
    def build_report(self, report: QualityReport) -> QualityReport:
        report.evaluate()
        return report

    def create_report(self, stage, scores: list[QualityScore], threshold: float, maximum_retry_count: int, reviewer_comments: list[str] | None = None, improvement_suggestions: list[str] | None = None, regeneration_count: int = 0) -> QualityReport:
        return self.build_report(QualityReport(stage=stage, scores=scores, threshold=threshold, maximum_retry_count=maximum_retry_count, reviewer_comments=reviewer_comments or [], improvement_suggestions=improvement_suggestions or [], regeneration_count=regeneration_count))

    def passes(self, report: QualityReport) -> bool:
        return self.build_report(report).status is QualityStatus.PASSED
