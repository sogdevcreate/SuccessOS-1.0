import unittest

from studio.enums import PipelineStage, StageStatus
from studio.models import DirectorsBible, ProductionProfile, ProjectMetadata, ProductionSettings, StudioProject
from studio.pipeline import StudioPipeline
from studio.research.citation import Citation
from studio.research.fact import Fact, VerificationStatus
from studio.research.research_report import ResearchReport
from studio.research.research_source import ResearchSource
from studio.screenwriting.character_arc import CharacterArc
from studio.screenwriting.continuity_checker import ContinuityChecker
from studio.screenwriting.dialogue_line import DialogueLine
from studio.screenwriting.narration_block import NarrationBlock
from studio.screenwriting.pacing_analyzer import PacingAnalyzer
from studio.screenwriting.screenplay import Screenplay
from studio.screenwriting.screenplay_beat import ScreenplayBeat
from studio.screenwriting.screenplay_engine import ScreenplayEngine
from studio.screenwriting.screenplay_pipeline import ScreenplayPipeline
from studio.screenwriting.screenplay_quality_reviewer import ScreenplayQualityReviewer
from studio.screenwriting.screenplay_scene import ScreenplayScene
from studio.screenwriting.screenplay_validator import ScreenplayValidator
from studio.screenwriting.story_structure import StoryStructure
from studio.services import InMemoryProjectRepository, PipelineStateManager, QualityManager, VersionManager


class ScreenwritingEngineTests(unittest.TestCase):
    def research(self) -> ResearchReport:
        return ResearchReport(topic="Historic mission", key_facts=[Fact("fact-1", "The mission launched in 1969.", ["source-1"], 0.95, VerificationStatus.VERIFIED), Fact("fact-2", "A disputed timeline detail.", ["source-1"], 0.5, VerificationStatus.DISPUTED)], sources=[ResearchSource("source-1", "Archive", reliability_score=9, relevance_score=9)], citations=[Citation("source-1", "p. 2")])

    def screenplay(self, genre="drama", audience="adults") -> Screenplay:
        first = ScreenplayScene("scene-1", 1, "INT. CONTROL ROOM - DAY", "Control Room", "Day", 60, ["Maya"], "Establish mission stakes", "Show glowing monitors", "Anticipation", "Maya studies the launch clock.", [DialogueLine("Maya", "We are ready.")], [NarrationBlock("The mission begins.")], ["CUT TO:"], ["fact-1", "fact-2"], [], ["fact-2"], ["Keep Maya's uniform blue."], ["Use restrained camera movement."], [ScreenplayBeat(1, "Launch countdown", "Hope rises", 7, ["fact-1"])])
        second = ScreenplayScene("scene-2", 2, "EXT. LAUNCH SITE - DAY", "Launch Site", "Day", 90, ["Maya"], "Deliver launch", "Show scale", "Awe", "The rocket ascends.", [DialogueLine("Maya", "Go.")], [], [], ["fact-1"], [], [], ["Maya remains in control room."], ["Use restrained camera movement."], [ScreenplayBeat(1, "Launch", "Awe", 9, ["fact-1"])])
        return Screenplay("Mission", "A crew faces history.", "A mission tests resolve.", genre, "hopeful", audience, "Can one launch change everything?", "The clock begins.", StoryStructure(["Act I", "Act II", "Act III"], ["Countdown", "Launch"], "The rocket clears the tower.", "The team reflects."), [second, first], [CharacterArc("Maya", "Doubt", "Confidence", ["Chooses to proceed"])], ["Doubt becomes resolve"], [], [], ["The clock returns"], ["The launch window is closing"], "Learn more in the archive.")

    def project(self, threshold=7.0, genre="drama", audience="adults") -> StudioProject:
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"), production_settings=ProductionSettings(quality_threshold=threshold), production_profile=ProductionProfile(genre=genre, audience=audience, duration=150), directors_bible=DirectorsBible(story_vision="A grounded account."), research_report=self.research(), screenplay=self.screenplay())
        project.stage_statuses[PipelineStage.RESEARCH] = StageStatus.SUCCEEDED
        return project

    def test_screenplay_serialization_and_scene_ordering(self) -> None:
        screenplay = self.screenplay()
        restored = Screenplay.from_dict(screenplay.to_dict())
        self.assertEqual([scene.id for scene in restored.ordered_scenes()], ["scene-1", "scene-2"])
        self.assertEqual(restored.climax, "The rocket clears the tower.")

    def test_runtime_and_pacing_calculation(self) -> None:
        screenplay = self.screenplay()
        self.assertEqual(screenplay.estimated_runtime_seconds, 150)
        self.assertEqual(PacingAnalyzer().analyze(screenplay), [7.0, 9.0])

    def test_research_traceability_and_disputed_claim_handling(self) -> None:
        screenplay = self.screenplay()
        self.assertEqual(ScreenplayValidator().validate(screenplay, self.research()), [])
        screenplay.scenes[1].disputed_fact_references = []
        errors = ScreenplayValidator().validate(screenplay, self.research())
        self.assertIn("does not identify disputed", errors[0])
        screenplay = self.screenplay()
        report = self.research()
        report.citations = []
        self.assertIn("without report citations", ScreenplayValidator().validate(screenplay, report)[0])

    def test_continuity_validation(self) -> None:
        screenplay = self.screenplay()
        self.assertEqual(ContinuityChecker().check(screenplay), [])
        screenplay.scenes[0].scene_number = 1
        self.assertTrue(ContinuityChecker().check(screenplay))

    def test_quality_scoring(self) -> None:
        project = self.project()
        report = ScreenplayQualityReviewer().review(project.screenplay, project.research_report, project.production_profile, project.directors_bible, 7.0)
        self.assertTrue(report.passed)
        self.assertEqual(len(report.scores), 13)

    def test_pipeline_quality_gate_and_version_snapshot(self) -> None:
        project = self.project()
        repository = InMemoryProjectRepository()
        engine = ScreenplayEngine(ScreenplayPipeline(), ScreenplayQualityReviewer())
        pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {PipelineStage.SCRIPT: engine})
        result = pipeline.run_stage(project, PipelineStage.SCRIPT)
        self.assertEqual(result.status, StageStatus.SUCCEEDED)
        self.assertEqual(len(project.version_history), 1)
        self.assertEqual(project.current_pipeline_stage, PipelineStage.STORYBOARD)

    def test_pipeline_rejects_screenplay_failing_quality_gate(self) -> None:
        project = self.project(threshold=9.5, genre="documentary")
        repository = InMemoryProjectRepository()
        pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {PipelineStage.SCRIPT: ScreenplayEngine(ScreenplayPipeline(), ScreenplayQualityReviewer())})
        result = pipeline.run_stage(project, PipelineStage.SCRIPT)
        self.assertEqual(result.status, StageStatus.FAILED)
        self.assertEqual(project.stage_statuses[PipelineStage.SCRIPT], StageStatus.FAILED)

    def test_storyboard_requires_approved_screenplay(self) -> None:
        project = self.project()
        repository = InMemoryProjectRepository()
        pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {})
        self.assertEqual(pipeline.run_stage(project, PipelineStage.STORYBOARD).status, StageStatus.FAILED)

    def test_legacy_project_deserialization_has_no_screenplay(self) -> None:
        project = self.project()
        data = project.to_dict()
        data.pop("screenplay")
        self.assertIsNone(StudioProject.from_dict(data).screenplay)


if __name__ == "__main__":
    unittest.main()
