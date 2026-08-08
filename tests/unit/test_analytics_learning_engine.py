import unittest

from studio.analytics.analytics_engine import AnalyticsEngine
from studio.analytics.analytics_provider_registry import AnalyticsProviderRegistry
from studio.analytics.analytics_provider_selector import AnalyticsProviderSelector
from studio.analytics.analytics_quality_reviewer import AnalyticsQualityReviewer
from studio.analytics.audience_metrics import AudienceMetrics
from studio.analytics.cost_metrics import CostMetrics
from studio.analytics.engagement_metrics import EngagementMetrics
from studio.analytics.feedback_record import FeedbackRecord
from studio.analytics.experiment import Experiment
from studio.analytics.experiment_variant import ExperimentVariant
from studio.analytics.learning_recommendation import LearningRecommendation, RecommendationState
from studio.analytics.learning_signal import LearningSignal
from studio.analytics.learning_report import LearningReport
from studio.analytics.learning_validator import LearningValidator
from studio.analytics.optimization_policy import OptimizationPolicy
from studio.analytics.performance_snapshot import PerformanceSnapshot
from studio.analytics.production_metrics import ProductionMetrics
from studio.analytics.retention_metrics import RetentionMetrics
from studio.enums import PipelineStage, ProjectStatus, StageStatus
from studio.models import ProjectMetadata, StudioProject
from studio.pipeline import StudioPipeline
from studio.pipeline import StageResult
from studio.publishing.publish_result import PublishResult, PublishResultStatus
from studio.services import InMemoryProjectRepository, PipelineStateManager, QualityManager, VersionManager


class AnalyticsLearningTests(unittest.TestCase):
    def snapshot(self):
        return PerformanceSnapshot("snapshot-1", "publication-1", "2030-01-01", "7d", "youtube", "provider", AudienceMetrics(views=100, geography={"NG": 100}), RetentionMetrics(average_view_duration=60.0, timeline_points=[(0.0, 100.0), (30.0, 80.0)]), EngagementMetrics(likes=20, engagement_rate=.2), production=ProductionMetrics(stage_durations={"rendering": 20.0}), cost=CostMetrics({"rendering": 4.0}, total_project_cost=4.0, currency="USD"), provenance={"provider": "test"})

    def signal(self):
        return LearningSignal("signal-1", ["views"], "project-1", "publication-1", "Observed aggregate retention", .8, "100 aggregate viewers", limitations=["single publication"], provenance={"snapshot": "snapshot-1"})

    def test_snapshot_round_trip_metrics_and_privacy(self):
        restored = PerformanceSnapshot.from_dict(self.snapshot().to_dict())
        self.assertEqual(restored.audience.geography, {"NG": 100})
        self.assertEqual(restored.audience.privacy_scope, "aggregate_only")
        self.assertEqual(restored.retention.timeline_points, [(0.0, 100.0), (30.0, 80.0)])
        self.assertEqual(restored.cost.currency, "USD")

    def test_recommendation_validation_and_approval_only_policy(self):
        signal = self.signal()
        recommendation = LearningRecommendation("recommendation-1", "Improve opening pacing", [signal.id], .7, "Better retention", ["limited sample"], "screenwriting", "Review opening hook", provenance={"report": "learning-1"})
        validator = LearningValidator()
        self.assertEqual(validator.validate_recommendation(recommendation, [signal]), [])
        with self.assertRaises(ValueError):
            OptimizationPolicy.from_approved_recommendation("policy-1", recommendation, "future_projects")
        recommendation.state = RecommendationState.APPROVED
        policy = OptimizationPolicy.from_approved_recommendation("policy-1", recommendation, "future_projects")
        self.assertTrue(policy.enabled)
        policy.disable()
        self.assertFalse(policy.enabled)

    def test_rejects_unsupported_evidence_and_causal_claims(self):
        invalid = LearningRecommendation("recommendation-2", "Claim", [], .9, "Benefit", [], "editing", "Change", causal_claim=True)
        errors = LearningValidator().validate_recommendation(invalid, [])
        self.assertIn("Recommendation requires supporting evidence", errors)
        self.assertIn("Unsupported causal claims are prohibited", errors)

    def test_experiment_and_project_round_trip_are_complete_and_legacy_safe(self):
        signal = self.signal()
        recommendation = LearningRecommendation("recommendation-1", "Rationale", [signal.id], .6, "Benefit", [], "titles", "Try variant", provenance={"signal": signal.id})
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"), performance_snapshots=[self.snapshot()], learning_recommendations=[recommendation], experiments=[Experiment("experiment-1", "Hypothesis", "ctr", [ExperimentVariant("control", "Control", control=True)])])
        restored = StudioProject.from_dict(project.to_dict())
        self.assertEqual(restored.performance_snapshots[0].audience.views, 100)
        self.assertEqual(restored.learning_recommendations[0].state, RecommendationState.PROPOSED)
        self.assertTrue(restored.experiments[0].variants[0].control)
        legacy = project.to_dict()
        for key in ("analytics_reports", "performance_snapshots", "learning_reports", "learning_recommendations", "optimization_policies", "experiments"): legacy.pop(key)
        legacy_restored = StudioProject.from_dict(legacy)
        self.assertEqual(legacy_restored.analytics_reports, [])
        self.assertEqual(legacy_restored.experiments, [])

    def test_post_publication_lifecycle_and_analytics_failure_isolation(self):
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"), publish_result=PublishResult(PublishResultStatus.COMPLETED, publication_reference="publication-1"))
        project.stage_statuses[PipelineStage.PUBLISH] = StageStatus.SUCCEEDED
        repository = InMemoryProjectRepository()
        pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {PipelineStage.ANALYTICS: AnalyticsEngine(AnalyticsProviderSelector(AnalyticsProviderRegistry()))})
        result = pipeline.run_stage(project, PipelineStage.ANALYTICS)
        self.assertEqual(result.status, StageStatus.FAILED)
        self.assertNotEqual(project.status, ProjectStatus.FAILED)
        self.assertTrue(project.analytics_reports[0].unavailable)
        self.assertEqual(pipeline.run_stage(project, PipelineStage.LEARNING).status, StageStatus.FAILED)

    def test_quality_reviewer_scores_analytics(self):
        report = AnalyticsQualityReviewer().review({criterion: 8.0 for criterion in AnalyticsQualityReviewer.criteria})
        self.assertEqual(report.stage, PipelineStage.ANALYTICS)
        self.assertEqual(report.overall_score, 8.0)

    def test_provider_selection_and_feedback_learning_report_serialization(self):
        class Provider:
            identity = "provider-1"; source = "youtube"
            def available(self): return True
        registry = AnalyticsProviderRegistry()
        registry.register(Provider(), priority=10)
        self.assertEqual(AnalyticsProviderSelector(registry).select("youtube").identity, "provider-1")
        signal = self.signal()
        recommendation = LearningRecommendation("recommendation-1", "Rationale", [signal.id], .7, "Benefit", [], "titles", "Review title", provenance={"signal": signal.id})
        report = LearningReport("learning-1", "analytics-1", observations=[signal.observation], hypotheses=["Test title"], signals=[signal], recommendations=[recommendation])
        restored = LearningReport.from_dict(report.to_dict())
        feedback = FeedbackRecord("feedback-1", "Director", "director-1", "2030-01-01", "Review title", {"project": "project-1"})
        self.assertEqual(restored.hypotheses, ["Test title"])
        self.assertEqual(FeedbackRecord.from_dict(feedback.to_dict()).source_type, "Director")

    def test_publish_analytics_learning_stage_order_with_successful_executors(self):
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"))
        project.stage_statuses[PipelineStage.PUBLISH] = StageStatus.SUCCEEDED
        repository = InMemoryProjectRepository()
        pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {
            PipelineStage.ANALYTICS: lambda _: StageResult(PipelineStage.ANALYTICS, StageStatus.SUCCEEDED),
            PipelineStage.LEARNING: lambda _: StageResult(PipelineStage.LEARNING, StageStatus.SUCCEEDED),
        })
        self.assertEqual(pipeline.run_stage(project, PipelineStage.ANALYTICS).status, StageStatus.SUCCEEDED)
        self.assertEqual(project.current_pipeline_stage, PipelineStage.LEARNING)
        self.assertEqual(pipeline.run_stage(project, PipelineStage.LEARNING).status, StageStatus.SUCCEEDED)


if __name__ == "__main__":
    unittest.main()
