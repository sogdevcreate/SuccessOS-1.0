import unittest

from studio.enums import AssetType, MediaType, PipelineStage, ProjectStatus, QualityStatus, StageStatus
from studio.models import Asset, ProjectMetadata, QualityReport, QualityScore, Research, StudioProject
from studio.pipeline import StageResult, StudioPipeline
from studio.services import InMemoryProjectRepository, PipelineStateManager, QualityManager, VersionManager


class StudioProjectTests(unittest.TestCase):
    def make_project(self) -> StudioProject:
        return StudioProject(metadata=ProjectMetadata(title="Studio Test", creator="Creator"))

    def test_project_creation_has_full_pipeline_state(self) -> None:
        project = self.make_project()
        self.assertEqual(project.status, ProjectStatus.DRAFT)
        self.assertEqual(project.current_pipeline_stage, PipelineStage.IDEA)
        self.assertEqual(set(project.stage_statuses), set(PipelineStage))

    def test_serialization_and_deserialization_round_trip(self) -> None:
        project = self.make_project()
        project.research = Research(topic="Space", findings=["fact"])
        project.assets.append(Asset("asset-1", AssetType.IMAGE, MediaType.IMAGE, "assets/image.png"))
        restored = StudioProject.from_dict(project.to_dict())
        self.assertEqual(restored.identifier, project.identifier)
        self.assertEqual(restored.research.topic, "Space")
        self.assertEqual(restored.assets[0].asset_type, AssetType.IMAGE)

    def test_enum_serialization(self) -> None:
        project = self.make_project()
        data = project.to_dict()
        self.assertEqual(data["status"], "draft")
        self.assertEqual(data["current_pipeline_stage"], "idea")


class VersionManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryProjectRepository()
        self.manager = VersionManager(self.repository)
        self.project = StudioProject(metadata=ProjectMetadata(title="Original", creator="Creator"))

    def test_create_list_compare_and_rollback(self) -> None:
        first = self.manager.create_snapshot(self.project, "initial")
        self.project.metadata.title = "Changed"
        second = self.manager.create_snapshot(self.project, "changed")
        self.assertEqual(len(self.manager.list_versions(self.project)), 2)
        comparison = self.manager.compare_versions(first, second)
        self.assertIn("metadata", comparison)
        restored = self.manager.rollback(self.project)
        self.assertEqual(restored.metadata.title, "Changed")
        restored = self.manager.restore_version(self.project, first.identifier)
        self.assertEqual(restored.metadata.title, "Original")


class QualityManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = QualityManager()

    def test_weighted_scoring_and_pass(self) -> None:
        report = QualityReport(PipelineStage.SCRIPT, [QualityScore("accuracy", 8, 3), QualityScore("style", 5, 1)], threshold=7)
        self.manager.build_report(report)
        self.assertEqual(report.overall_score, 7.25)
        self.assertEqual(report.status, QualityStatus.PASSED)

    def test_quality_gate_fail_and_retry_limit(self) -> None:
        report = QualityReport(PipelineStage.SCRIPT, [QualityScore("accuracy", 5)], threshold=7, regeneration_count=2, maximum_retry_count=2)
        self.assertFalse(self.manager.passes(report))
        self.assertEqual(report.status, QualityStatus.RETRY_EXHAUSTED)


class StudioPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryProjectRepository()
        self.versions = VersionManager(self.repository)
        self.quality = QualityManager()
        self.states = PipelineStateManager()
        self.project = StudioProject(metadata=ProjectMetadata(title="Pipeline", creator="Creator"))

    def pipeline(self, executors=None) -> StudioPipeline:
        return StudioPipeline(self.repository, self.versions, self.quality, self.states, executors)

    @staticmethod
    def success(stage: PipelineStage, quality_report=None):
        return lambda context: StageResult(stage, StageStatus.SUCCEEDED, quality_report=quality_report)

    def test_stage_ordering_and_snapshot_after_success(self) -> None:
        self.assertEqual(StudioPipeline.STAGES, tuple(PipelineStage))
        pipeline = self.pipeline({PipelineStage.IDEA: self.success(PipelineStage.IDEA)})
        result = pipeline.run_stage(self.project)
        self.assertEqual(result.status, StageStatus.SUCCEEDED)
        self.assertEqual(self.project.current_pipeline_stage, PipelineStage.RESEARCH)
        self.assertEqual(len(self.project.version_history), 1)

    def test_pause_resume_and_cancel(self) -> None:
        pipeline = self.pipeline()
        pipeline.pause(self.project)
        self.assertEqual(pipeline.run_stage(self.project).status, StageStatus.PAUSED)
        pipeline.resume(self.project)
        self.assertEqual(self.project.status, ProjectStatus.ACTIVE)
        pipeline.cancel(self.project)
        self.assertEqual(self.project.status, ProjectStatus.CANCELLED)

    def test_failed_stage_and_retry(self) -> None:
        pipeline = self.pipeline({PipelineStage.IDEA: lambda context: StageResult.failed(PipelineStage.IDEA, "provider unavailable")})
        self.assertEqual(pipeline.run_stage(self.project).status, StageStatus.FAILED)
        self.assertEqual(self.project.stage_statuses[PipelineStage.IDEA], StageStatus.FAILED)
        self.assertEqual(pipeline.retry_failed_stage(self.project).status, StageStatus.FAILED)

    def test_optional_stage_skipping(self) -> None:
        pipeline = self.pipeline()
        pipeline.skip_optional_stage(self.project, PipelineStage.MUSIC_SFX)
        self.assertEqual(self.project.stage_statuses[PipelineStage.MUSIC_SFX], StageStatus.SKIPPED)
        with self.assertRaises(ValueError):
            pipeline.skip_optional_stage(self.project, PipelineStage.SCRIPT)

    def test_quality_gate_blocks_advance(self) -> None:
        report = QualityReport(PipelineStage.IDEA, [QualityScore("idea", 3)], threshold=7)
        pipeline = self.pipeline({PipelineStage.IDEA: self.success(PipelineStage.IDEA, report)})
        result = pipeline.run_stage(self.project)
        self.assertEqual(result.status, StageStatus.FAILED)
        self.assertEqual(self.project.current_pipeline_stage, PipelineStage.IDEA)

    def test_dependency_injection_construction(self) -> None:
        pipeline = self.pipeline({})
        self.assertIsInstance(pipeline, StudioPipeline)
        self.assertIs(self.repository.get(self.project.identifier), None)


if __name__ == "__main__":
    unittest.main()
