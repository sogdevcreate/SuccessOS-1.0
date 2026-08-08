from studio.enums import PipelineStage
from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore
from studio.research.research_report import ResearchReport


class ResearchQualityReviewer:
    CRITERIA = ("factual_reliability", "source_diversity", "source_quality", "completeness", "contradiction_handling", "citation_coverage", "storytelling_usefulness", "visual_usefulness")

    def review(self, report: ResearchReport, threshold: float, maximum_retry_count: int = 2, regeneration_count: int = 0) -> QualityReport:
        scores = [QualityScore(criterion, self._score(criterion, report)) for criterion in self.CRITERIA]
        quality_report = QualityReport(stage=PipelineStage.RESEARCH, scores=scores, threshold=threshold, maximum_retry_count=maximum_retry_count, regeneration_count=regeneration_count)
        quality_report.evaluate()
        return quality_report

    def _score(self, criterion: str, report: ResearchReport) -> float:
        source_ids = {source.identifier for source in report.sources}
        if criterion == "factual_reliability":
            return self._average([fact.confidence * 10 for fact in report.verified_facts])
        if criterion == "source_diversity":
            return min(10.0, len({source.source_type for source in report.sources}) * 2.5)
        if criterion == "source_quality":
            return self._average([source.reliability_score for source in report.sources])
        if criterion == "completeness":
            fields = [report.executive_summary, report.research_questions, report.key_facts, report.timeline, report.entities, report.sources]
            return 10.0 * sum(bool(field) for field in fields) / len(fields)
        if criterion == "contradiction_handling":
            return 10.0 if not report.contradictions else 10.0 * sum(bool(first and second) for first, second in report.contradictions) / len(report.contradictions)
        if criterion == "citation_coverage":
            cited_source_ids = {citation.source_id for citation in report.citations}
            supported = [fact for fact in report.key_facts if fact.source_references and set(fact.source_references).issubset(source_ids) and set(fact.source_references).intersection(cited_source_ids)]
            return 10.0 * len(supported) / len(report.key_facts) if report.key_facts else 0.0
        if criterion == "storytelling_usefulness":
            fields = [report.themes, report.script_angles, report.hook_ideas]
            return 10.0 * sum(bool(field) for field in fields) / len(fields)
        return min(10.0, 10.0 * sum(bool(field) for field in [report.visual_opportunities, report.suggested_scenes, report.suggested_archive_reference_needs]) / 3)

    @staticmethod
    def _average(values: list[float]) -> float:
        return sum(values) / len(values) if values else 0.0
