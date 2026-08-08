import unittest

from studio.enums import PipelineStage, StageStatus
from studio.models import DirectorsBible, ProductionProfile, ProjectMetadata, ProductionSettings, StudioProject
from studio.pipeline import StudioPipeline
from studio.screenwriting.screenplay import Screenplay
from studio.screenwriting.screenplay_scene import ScreenplayScene
from studio.services import InMemoryProjectRepository, PipelineStateManager, QualityManager, VersionManager
from studio.storyboard.blocking_plan import BlockingPlan
from studio.storyboard.camera_plan import CameraPlan
from studio.storyboard.composition_plan import CompositionPlan
from studio.storyboard.lens_profile import LensProfile
from studio.storyboard.lighting_plan import LightingPlan
from studio.storyboard.shot import Shot
from studio.storyboard.shot_sequence import ShotSequence
from studio.storyboard.storyboard import CinematicStoryboard
from studio.storyboard.storyboard_engine import StoryboardEngine
from studio.storyboard.storyboard_pipeline import StoryboardPipeline
from studio.storyboard.storyboard_quality_reviewer import StoryboardQualityReviewer
from studio.storyboard.storyboard_scene import StoryboardScene
from studio.storyboard.storyboard_validator import StoryboardValidator
from studio.storyboard.transition_plan import TransitionPlan
from studio.storyboard.visual_continuity import VisualContinuity


class StoryboardCinematographyTests(unittest.TestCase):
    def screenplay(self) -> Screenplay:
        return Screenplay("Film", scenes=[ScreenplayScene("scene-1", 1, "INT. ROOM - DAY", "Room", "Day", 60), ScreenplayScene("scene-2", 2, "EXT. STREET - NIGHT", "Street", "Night", 90)])

    def shot(self, identifier, scene_id, number, shot_type="wide", duration=60) -> Shot:
        return Shot(identifier, scene_id, f"seq-{scene_id}", number, shot_type, CompositionPlan("wide", "eye level", "eye level", "cool", "tense"), CameraPlan("doorway", "Maya", "dolly", LensProfile("prime", 35, "f/2.8", "shallow"), "steadicam", "slow", "opening", ["rack focus to Maya"]), BlockingPlan(["Maya centre"], ["Maya crosses left to right"], "left-to-right", "Maya-to-door"), ["period room"], ["blue coat"], LightingPlan("soft key", "negative fill", "rim", ["lamp"], "window", "daylight", "protect highlights", "medium", "soft", "5600K", "tense"), duration, TransitionPlan("cut", "dissolve"), "00:00-00:05", [], VisualContinuity(["Maya blue coat"], ["room"], ["blue coat"], ["letter"], ["cool key"], True, "Maya-to-door"), [scene_id])

    def storyboard(self) -> CinematicStoryboard:
        first = self.shot("shot-1", "scene-1", 2, "close-up", 30)
        second = self.shot("shot-2", "scene-1", 1, "wide", 30)
        third = self.shot("shot-3", "scene-2", 1, "tracking", 90)
        return CinematicStoryboard("Film", [StoryboardScene("scene-1", ShotSequence("seq-scene-1", "scene-1", [first, second]), "Maya's uncertainty becomes visible."), StoryboardScene("scene-2", ShotSequence("seq-scene-2", "scene-2", [third]), "The city mirrors Maya's resolve.")])

    def project(self, threshold=7.0) -> StudioProject:
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"), production_settings=ProductionSettings(quality_threshold=threshold), production_profile=ProductionProfile(visual_style="cinematic", realism_level="photorealistic"), directors_bible=DirectorsBible(story_vision="A grounded journey.", visual_rules=["Naturalistic light"]), screenplay=self.screenplay(), cinematic_storyboard=self.storyboard())
        project.stage_statuses[PipelineStage.SCRIPT] = StageStatus.SUCCEEDED
        return project

    def test_shot_ordering_and_serialization(self) -> None:
        storyboard = self.storyboard()
        self.assertEqual([shot.id for shot in storyboard.scenes[0].sequence.ordered_shots()], ["shot-2", "shot-1"])
        restored = CinematicStoryboard.from_dict(storyboard.to_dict())
        self.assertEqual(restored.shots[0].camera_plan.lens_profile.focal_length_mm, 35)

    def test_camera_and_lighting_plan_serialization(self) -> None:
        shot = self.shot("shot", "scene-1", 1)
        restored = Shot.from_dict(shot.to_dict())
        self.assertEqual(restored.camera_plan.focus_transitions, ["rack focus to Maya"])
        self.assertEqual(restored.lighting_plan.color_temperature, "5600K")

    def test_scene_screenplay_traceability_and_180_degree_metadata(self) -> None:
        storyboard = self.storyboard()
        self.assertEqual(StoryboardValidator().validate(storyboard, self.screenplay()), [])
        self.assertTrue(storyboard.shots[0].continuity.preserve_180_degree_rule)
        storyboard.shots[1].scene_id = "unknown"
        self.assertTrue(StoryboardValidator().validate(storyboard, self.screenplay()))

    def test_runtime_consistency(self) -> None:
        self.assertEqual(self.storyboard().estimated_runtime_seconds, self.screenplay().estimated_runtime_seconds)

    def test_quality_scoring(self) -> None:
        project = self.project()
        report = StoryboardQualityReviewer().review(project.cinematic_storyboard, project.screenplay, project.production_profile, project.directors_bible, 7.0)
        self.assertTrue(report.passed)
        self.assertEqual(len(report.scores), 14)

    def test_pipeline_integration_quality_gate_and_snapshot(self) -> None:
        project = self.project()
        repository = InMemoryProjectRepository()
        pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {PipelineStage.STORYBOARD: StoryboardEngine(StoryboardPipeline(), StoryboardQualityReviewer())})
        result = pipeline.run_stage(project, PipelineStage.STORYBOARD)
        self.assertEqual(result.status, StageStatus.SUCCEEDED)
        self.assertEqual(len(project.version_history), 1)
        self.assertEqual(project.current_pipeline_stage, PipelineStage.CHARACTERS)

    def test_quality_gate_failure_and_downstream_guard(self) -> None:
        project = self.project(threshold=9.9)
        repository = InMemoryProjectRepository()
        pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {PipelineStage.STORYBOARD: StoryboardEngine(StoryboardPipeline(), StoryboardQualityReviewer())})
        self.assertEqual(pipeline.run_stage(project, PipelineStage.STORYBOARD).status, StageStatus.FAILED)
        self.assertEqual(pipeline.run_stage(project, PipelineStage.ASSETS).status, StageStatus.FAILED)

    def test_legacy_project_has_no_cinematic_storyboard(self) -> None:
        data = self.project().to_dict()
        data.pop("cinematic_storyboard")
        self.assertIsNone(StudioProject.from_dict(data).cinematic_storyboard)


if __name__ == "__main__":
    unittest.main()
