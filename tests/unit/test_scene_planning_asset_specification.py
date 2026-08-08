import unittest
from studio.continuity.continuity_registry import ContinuityRegistry
from studio.enums import PipelineStage, StageStatus
from studio.models import DirectorsBible, ProductionProfile, ProjectMetadata, StudioProject
from studio.pipeline import StudioPipeline
from studio.scene_planning.asset_spec_validator import AssetSpecValidator
from studio.scene_planning.asset_specification import AssetSpecification
from studio.scene_planning.character_asset_spec import CharacterAssetSpec
from studio.scene_planning.environment_asset_spec import EnvironmentAssetSpec
from studio.scene_planning.generation_instruction import GenerationInstruction
from studio.scene_planning.prop_asset_spec import PropAssetSpec
from studio.scene_planning.provider_capability import ProviderCapability
from studio.scene_planning.reference_binding import ReferenceBinding
from studio.scene_planning.scene_plan import ScenePlan
from studio.scene_planning.scene_planner import ScenePlanningEngine
from studio.scene_planning.scene_quality_reviewer import SceneQualityReviewer
from studio.scene_planning.scene_validator import SceneValidator
from studio.screenwriting.screenplay import Screenplay
from studio.screenwriting.screenplay_scene import ScreenplayScene
from studio.services import InMemoryProjectRepository, PipelineStateManager, QualityManager, VersionManager
from studio.storyboard.shot_sequence import ShotSequence
from studio.storyboard.storyboard import CinematicStoryboard
from studio.storyboard.storyboard_scene import StoryboardScene

class ScenePlanningTests(unittest.TestCase):
    def spec(self):
        return AssetSpecification("maya-asset", "character", ["plan-1"], ["shot-1"], ["script"], "Photorealistic Maya in blue coat", "wool coat", ["photorealistic"], "4K", "16:9", "cinematic", ["keep brown eyes"], [ReferenceBinding("maya", "identity_lock", "identity")], ["maya-lock"], ["wrong eye color"], GenerationInstruction(["text-to-image"], "Maya under rain light", "cartoon, altered identity", True, False, False, False, True, "cinematic", 1, 0, 0, "4K", "16:9"), [], ["retry only if lock mismatch"], ["matches identity lock"])
    def project(self, threshold=7.0):
        screenplay = Screenplay("Film", scenes=[ScreenplayScene("scene-1", 1, "INT. ROOM - NIGHT", "Room", "Night", 60)])
        storyboard = CinematicStoryboard("Film", [StoryboardScene("scene-1", ShotSequence("board-1", "scene-1", []), "Rain-lit close-up")])
        plan = ScenePlan("plan-1", "scene-1", "scene-1", 60, "Room", "night", "rain", ["maya"], ["coat-1"], ["mission-clock"], ["intact"], "cool rain light", ["shot-1"], "0-10", "", ["rain"], [], ["maya-lock"], ["maya-asset"], ["maya-asset"], [], ["rain reflection"], [])
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"), production_profile=ProductionProfile(realism_level="photorealistic", visual_style="cinematic"), directors_bible=DirectorsBible(story_vision="Grounded", visual_rules=["naturalistic"]), screenplay=screenplay, cinematic_storyboard=storyboard, continuity_registry=ContinuityRegistry(), scene_plans=[plan], asset_specifications=[self.spec()])
        project.production_settings.quality_threshold = threshold; project.stage_statuses[PipelineStage.STORYBOARD] = StageStatus.SUCCEEDED; project.stage_statuses[PipelineStage.CHARACTERS] = StageStatus.SUCCEEDED
        return project
    def test_serialization_bindings_and_instruction(self):
        spec = AssetSpecification.from_dict(self.spec().to_dict()); self.assertEqual(spec.generation_instruction.aspect_ratio, "16:9")
        self.assertEqual(CharacterAssetSpec(spec, "maya", "face", "body", "coat", "maya-lock", "calm").visual_identity_lock_binding, "maya-lock")
        self.assertEqual(EnvironmentAssetSpec(spec, "room", "room", "set", "rain", "night", "cool", "intact").weather, "rain")
        self.assertEqual(PropAssetSpec(spec, "clock", "Maya", "room", "intact", ["scene-1"]).current_location, "room")
    def test_provider_capability_matching_and_rejection(self):
        capability = ProviderCapability("future", {"text-to-image"}, character_reference=True, supported_aspect_ratios={"16:9"})
        self.assertEqual(AssetSpecValidator().validate_provider(self.spec(), capability), [])
        self.assertTrue(AssetSpecValidator().validate_provider(self.spec(), ProviderCapability("limited")))
    def test_quality_pipeline_snapshot_and_gate_failure(self):
        project = self.project(); repository = InMemoryProjectRepository(); pipeline = StudioPipeline(repository, VersionManager(repository), QualityManager(), PipelineStateManager(), {PipelineStage.SCENE_PLANNING: ScenePlanningEngine(SceneValidator(), SceneQualityReviewer())})
        self.assertEqual(pipeline.run_stage(project, PipelineStage.SCENE_PLANNING).status, StageStatus.SUCCEEDED); self.assertEqual(len(project.version_history), 1)
        failed = self.project(10.1); self.assertEqual(pipeline.run_stage(failed, PipelineStage.SCENE_PLANNING).status, StageStatus.FAILED)
    def test_backward_compatibility(self):
        data = self.project().to_dict(); data.pop("scene_plans"); data.pop("asset_specifications"); restored = StudioProject.from_dict(data); self.assertEqual(restored.scene_plans, []); self.assertEqual(restored.asset_specifications, [])
if __name__ == "__main__": unittest.main()
