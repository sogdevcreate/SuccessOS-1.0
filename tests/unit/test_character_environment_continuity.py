import unittest

from studio.continuity.body_profile import BodyProfile
from studio.continuity.character_engine import CharacterEnvironmentContinuityEngine
from studio.continuity.character_identity import CharacterIdentity
from studio.continuity.character_profile import CharacterProfile
from studio.continuity.character_quality_reviewer import CharacterQualityReviewer
from studio.continuity.continuity_registry import ContinuityRegistry
from studio.continuity.continuity_validator import ContinuityValidator
from studio.continuity.environment_profile import EnvironmentProfile
from studio.continuity.environment_quality_reviewer import EnvironmentQualityReviewer
from studio.continuity.facial_profile import FacialProfile
from studio.continuity.location_profile import LocationProfile
from studio.continuity.prop_profile import PropProfile
from studio.continuity.set_profile import SetProfile
from studio.continuity.visual_identity_lock import VisualIdentityLock
from studio.continuity.voice_identity import VoiceIdentity
from studio.continuity.wardrobe_profile import WardrobeProfile
from studio.enums import PipelineStage, StageStatus
from studio.models import DirectorsBible, ProductionProfile, ProjectMetadata, StudioProject
from studio.pipeline import StudioPipeline
from studio.services import InMemoryProjectRepository, PipelineStateManager, QualityManager, VersionManager
from studio.storyboard.storyboard import CinematicStoryboard


class CharacterEnvironmentContinuityTests(unittest.TestCase):
    def registry(self) -> ContinuityRegistry:
        character = CharacterProfile(CharacterIdentity("maya", "Maya", "30s", "woman", ["Nigerian"]), FacialProfile(face_shape="oval", eyes="brown", skin_texture="natural"), BodyProfile(height="170 cm", build="athletic", posture="upright"), ["touches watch"], [WardrobeProfile("coat-1", ["scene-1"], ["coat"], ["blue"], ["wool"], "clean", "dry", ["watch"], ["kept through scene-2"])], ["watch"], ["small scar"], "adult", "calm", VoiceIdentity("voice-maya", "warm", "measured"), VisualIdentityLock(["asset-maya"], ["handle-maya"], {"seed": "42"}, ["oval face", "blue coat"], ["different eye color"], {"eyes": "brown", "hair": "black"}), ["Keep scar on left brow."])
        environment = EnvironmentProfile(LocationProfile("control-room", "Lagos", "modern concrete", "2026"), SetProfile("two desks", ["concrete"], ["blue", "gray"], ["desk"], []), "rain", "wet season", "night", "cool practicals", ["mission clock"], "intact", ["rain continues from previous scene"])
        prop = PropProfile("mission-clock", "analog clock", "20cm", "metal", "Maya", "control-room", ["scene-1"], "intact", ["on desk"])
        return ContinuityRegistry({"maya": character}, {"control-room": environment}, {"mission-clock": prop})

    def project(self, threshold=7.0) -> StudioProject:
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"), production_profile=ProductionProfile(realism_level="photorealistic", visual_style="cinematic"), directors_bible=DirectorsBible(story_vision="Grounded drama", character_rules=["Maya remains reserved"], visual_rules=["Natural light"], lighting_rules=["Cool rain light"]), cinematic_storyboard=CinematicStoryboard("Film"), continuity_registry=self.registry())
        project.stage_statuses[PipelineStage.STORYBOARD] = StageStatus.SUCCEEDED
        project.production_settings.quality_threshold = threshold
        return project

    def test_character_environment_and_identity_lock_serialization(self) -> None:
        registry = self.registry()
        restored = ContinuityRegistry.from_dict(registry.to_dict())
        self.assertEqual(restored.characters["maya"].visual_identity_lock.seed_metadata, {"seed": "42"})
        self.assertEqual(restored.environments["control-room"].weather, "rain")
        self.assertEqual(restored.characters["maya"].wardrobe[0].costume_id, "coat-1")

    def test_prop_state_snapshot_restore_and_damage_progression(self) -> None:
        registry = self.registry()
        snapshot = registry.create_snapshot("scene-1")
        registry.props["mission-clock"].damage_state = "cracked"
        registry.props["mission-clock"].current_location = "street"
        registry.restore(snapshot)
        self.assertEqual(registry.props["mission-clock"].damage_state, "intact")
        self.assertEqual(registry.props["mission-clock"].current_location, "control-room")

    def test_identity_drift_time_and_weather_conflicts(self) -> None:
        registry = self.registry()
        first = registry.create_snapshot("scene-1")
        registry.characters["maya"].age_progression_state = "elderly"
        registry.environments["control-room"].time_of_day = "day"
        registry.environments["control-room"].weather = "sunny"
        second = registry.create_snapshot("scene-2")
        errors = ContinuityValidator().detect_drift(first, second)
        self.assertTrue(any("appearance drift" in error for error in errors))
        self.assertTrue(any("Time-of-day" in error for error in errors))
        self.assertTrue(any("Weather" in error for error in errors))

    def test_quality_scoring_and_pipeline_integration(self) -> None:
        project = self.project()
        repository = InMemoryProjectRepository()
        engine = CharacterEnvironmentContinuityEngine(ContinuityValidator(), CharacterQualityReviewer(), EnvironmentQualityReviewer())
        pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {PipelineStage.CHARACTERS: engine})
        result = pipeline.run_stage(project, PipelineStage.CHARACTERS)
        self.assertEqual(result.status, StageStatus.SUCCEEDED)
        self.assertEqual(len(project.version_history), 1)
        self.assertEqual(project.current_pipeline_stage, PipelineStage.SCENE_PLANNING)

    def test_quality_gate_failure_and_assets_guard(self) -> None:
        project = self.project(threshold=10.1)
        repository = InMemoryProjectRepository()
        engine = CharacterEnvironmentContinuityEngine(ContinuityValidator(), CharacterQualityReviewer(), EnvironmentQualityReviewer())
        pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {PipelineStage.CHARACTERS: engine})
        self.assertEqual(pipeline.run_stage(project, PipelineStage.CHARACTERS).status, StageStatus.FAILED)
        self.assertEqual(pipeline.run_stage(project, PipelineStage.ASSETS).status, StageStatus.FAILED)

    def test_legacy_project_compatibility(self) -> None:
        data = self.project().to_dict()
        for key in ("character_profiles", "environment_profiles", "prop_profiles", "continuity_registry"):
            data.pop(key)
        restored = StudioProject.from_dict(data)
        self.assertEqual(restored.character_profiles, [])
        self.assertIsNone(restored.continuity_registry)


if __name__ == "__main__": unittest.main()
