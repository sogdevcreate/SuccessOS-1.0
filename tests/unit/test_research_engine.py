import unittest
from datetime import date

from studio.enums import PipelineStage, StageStatus
from studio.models import ProjectMetadata, StudioProject
from studio.pipeline import StageResult, StudioPipeline
from studio.research.citation import Citation
from studio.research.contradiction_detector import ContradictionDetector
from studio.research.entity import Entity, EntityType
from studio.research.fact import Fact, VerificationStatus
from studio.research.research_engine import ResearchEngine
from studio.research.research_pipeline import ResearchPipeline
from studio.research.research_quality_reviewer import ResearchQualityReviewer
from studio.research.research_report import ResearchReport
from studio.research.research_source import ResearchSource, SourceType
from studio.research.source_ranker import SourceRanker
from studio.research.timeline_event import TimelineEvent
from studio.services import InMemoryProjectRepository, PipelineStateManager, QualityManager, VersionManager


class ResearchEngineTests(unittest.TestCase):
    def source(self, identifier="primary", source_type=SourceType.PRIMARY, reliability=9.0, relevance=9.0):
        return ResearchSource(identifier, "Evidence", publisher="Archive", url="https://example.test/evidence", publication_date=date(2020, 1, 1), accessed_date=date(2026, 8, 8), source_type=source_type, reliability_score=reliability, relevance_score=relevance, citation_metadata={"format": "web"})

    def report(self) -> ResearchReport:
        return ResearchReport(topic="The moon landing", research_questions=["What happened?"], executive_summary="A documented historical event.", key_facts=[Fact("fact-1", "The mission landed in 1969.", ["primary"], 0.9, VerificationStatus.VERIFIED)], timeline=[TimelineEvent(date(1970, 1, 1), "Later event", ["primary"], 0.8), TimelineEvent(date(1969, 7, 20), "Landing", ["primary"], 0.95)], entities=[Entity("Apollo 11", EntityType.ORGANIZATION, ["primary"], 0.9)], sources=[self.source(), self.source("journal", SourceType.JOURNALISM, 8.0, 8.0)], citations=[Citation("primary", "p. 1")], themes=["exploration"], visual_opportunities=["archival launch footage"], suggested_scenes=["launch"], suggested_archive_reference_needs=["mission footage"], script_angles=["human achievement"], hook_ideas=["One small step"], thumbnail_ideas=["moon and capsule"])

    def test_source_ranking(self) -> None:
        lower = self.source("lower", reliability=5.0, relevance=5.0)
        ranked = SourceRanker().rank([lower, self.source()])
        self.assertEqual(ranked[0].identifier, "primary")

    def test_citation_serialization(self) -> None:
        citation = Citation("source", "p. 10", "quoted", {"edition": "first"})
        self.assertEqual(Citation.from_dict(citation.to_dict()), citation)

    def test_fact_verification_state_and_confidence(self) -> None:
        fact = Fact("fact", "Claim", ["source"], 0.75, VerificationStatus.DISPUTED)
        self.assertTrue(fact.disputed)
        self.assertEqual(Fact.from_dict(fact.to_dict()).verification_status, VerificationStatus.DISPUTED)
        with self.assertRaises(ValueError):
            Fact("bad", "Claim", ["source"], 1.1)

    def test_contradiction_detection_links_facts(self) -> None:
        first = Fact("first", "The event occurred in 1969.", ["primary"], 0.9, VerificationStatus.VERIFIED)
        second = Fact("second", "the event occurred in 1969.", ["journal"], 0.5, VerificationStatus.DISPUTED)
        pairs = ContradictionDetector().detect([first, second])
        self.assertEqual(pairs, [("first", "second")])
        self.assertEqual(first.contradiction_references, ["second"])

    def test_timeline_ordering_and_report_round_trip(self) -> None:
        report = self.report()
        self.assertEqual(report.ordered_timeline()[0].event_date, date(1969, 7, 20))
        restored = ResearchReport.from_dict(report.to_dict())
        self.assertEqual(restored.people, [])
        self.assertEqual(restored.verified_facts[0].identifier, "fact-1")
        self.assertEqual(restored.sources[0].source_type, SourceType.PRIMARY)

    def test_quality_scoring_and_gate_outcomes(self) -> None:
        reviewer = ResearchQualityReviewer()
        passing = reviewer.review(self.report(), threshold=7.0)
        self.assertGreaterEqual(passing.overall_score, 7.0)
        self.assertTrue(passing.passed)
        failing = reviewer.review(ResearchReport(topic="Bare"), threshold=7.0)
        self.assertFalse(failing.passed)

    def test_pipeline_integration_and_script_prerequisite(self) -> None:
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"), research_report=self.report())
        repository = InMemoryProjectRepository()
        pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {PipelineStage.RESEARCH: ResearchEngine(ResearchPipeline(), ResearchQualityReviewer()), PipelineStage.SCRIPT: lambda context: StageResult(PipelineStage.SCRIPT, StageStatus.SUCCEEDED)})
        blocked = pipeline.run_stage(project, PipelineStage.SCRIPT)
        self.assertEqual(blocked.status, StageStatus.FAILED)
        result = pipeline.run_stage(project, PipelineStage.RESEARCH)
        self.assertEqual(result.status, StageStatus.SUCCEEDED)
        self.assertIs(project.research_report, project.research_report)
        self.assertEqual(pipeline.run_stage(project, PipelineStage.SCRIPT).status, StageStatus.SUCCEEDED)

    def test_pipeline_rejects_research_that_fails_quality_gate(self) -> None:
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"), research_report=ResearchReport(topic="Bare"))
        repository = InMemoryProjectRepository()
        pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {PipelineStage.RESEARCH: ResearchEngine(ResearchPipeline(), ResearchQualityReviewer())})
        result = pipeline.run_stage(project, PipelineStage.RESEARCH)
        self.assertEqual(result.status, StageStatus.FAILED)
        self.assertEqual(project.stage_statuses[PipelineStage.RESEARCH], StageStatus.FAILED)

    def test_legacy_project_deserialization_has_no_research_report(self) -> None:
        project = StudioProject(metadata=ProjectMetadata("Legacy", "Creator"))
        data = project.to_dict()
        data.pop("research_report")
        self.assertIsNone(StudioProject.from_dict(data).research_report)


if __name__ == "__main__":
    unittest.main()
