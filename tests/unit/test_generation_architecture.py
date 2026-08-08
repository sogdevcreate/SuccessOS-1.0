import unittest
from studio.enums import PipelineStage, StageStatus
from studio.generation.asset_generation_engine import AssetGenerationEngine
from studio.generation.asset_quality_reviewer import AssetQualityReviewer
from studio.generation.generation_job import GenerationJob, JobStatus
from studio.generation.generation_pipeline import GenerationPipeline
from studio.generation.generation_provider_registry import GenerationProviderRegistry, ProviderRecord
from studio.generation.generation_queue import GenerationQueue
from studio.generation.generation_request import GenerationRequest
from studio.generation.generated_asset import GeneratedAsset
from studio.generation.generation_validator import GenerationValidator
from studio.generation.provider_selector import ProviderSelector
from studio.models import DirectorsBible, ProductionProfile, ProjectMetadata, StudioProject
from studio.pipeline import StudioPipeline
from studio.scene_planning.asset_specification import AssetSpecification
from studio.scene_planning.generation_instruction import GenerationInstruction
from studio.scene_planning.provider_capability import ProviderCapability
from studio.services import InMemoryProjectRepository, PipelineStateManager, QualityManager, VersionManager
class FakeProvider:
    identity="test"; capabilities=ProviderCapability("test", {"text-to-image"}, character_reference=True, supported_aspect_ratios={"16:9"})
    def available(self): return True
class GenerationArchitectureTests(unittest.TestCase):
 def spec(self): return AssetSpecification("asset-1","character",visual_description="photo",identity_locks=["lock"],acceptance_criteria=["match"],generation_instruction=GenerationInstruction(["text-to-image"],"photo","cartoon",True,aspect_ratio="16:9"))
 def request(self): return GenerationRequest(self.spec(),ProductionProfile(realism_level="photorealistic"),DirectorsBible(),["lock"],["snapshot"],deterministic_metadata={"seed":"1"})
 def test_request_provenance_and_provider_selection(self):
  request=self.request(); restored=GenerationRequest.from_dict(request.to_dict(),request.production_profile,request.directors_bible); self.assertEqual(restored.deterministic_metadata,{"seed":"1"})
  registry=GenerationProviderRegistry(); registry.register(ProviderRecord(FakeProvider(),priority=1,quality_metadata={"photorealism":10,"reliability":10})); self.assertEqual(ProviderSelector(registry).select(request).identity,"test")
  self.assertIsNone(ProviderSelector(GenerationProviderRegistry()).select(request))
 def test_job_queue_retry_cancel(self):
  job=GenerationJob("r"); job.transition(JobStatus.RUNNING); job.transition(JobStatus.FAILED); job.transition(JobStatus.RETRYING); job.transition(JobStatus.RUNNING); job.transition(JobStatus.CANCELLED); self.assertEqual(job.status,JobStatus.CANCELLED)
 def test_asset_acceptance_pipeline_and_animation_gate(self):
  request=self.request(); registry=GenerationProviderRegistry(); registry.register(ProviderRecord(FakeProvider(),quality_metadata={"photorealism":10,"reliability":10})); pipeline_impl=GenerationPipeline(ProviderSelector(registry),GenerationQueue(),GenerationValidator())
  asset=GeneratedAsset("g","asset-1","scene",["shot"],"character","image",reference_uri="memory://g",provider="test",generation_request_id=request.id,provenance={"validated":"true","seed":"1"})
  project=StudioProject(metadata=ProjectMetadata("Film","Creator"),asset_specifications=[self.spec()],generation_requests=[request],generated_assets=[asset]); project.stage_statuses[PipelineStage.STORYBOARD]=StageStatus.SUCCEEDED; project.stage_statuses[PipelineStage.CHARACTERS]=StageStatus.SUCCEEDED; project.stage_statuses[PipelineStage.SCENE_PLANNING]=StageStatus.SUCCEEDED
  pipeline=StudioPipeline(InMemoryProjectRepository(),VersionManager(InMemoryProjectRepository()),QualityManager(),PipelineStateManager(),{PipelineStage.ASSETS:AssetGenerationEngine(pipeline_impl,AssetQualityReviewer())})
  self.assertEqual(pipeline.run_stage(project,PipelineStage.ASSETS).status,StageStatus.SUCCEEDED); self.assertTrue(asset.accepted); self.assertEqual(pipeline.run_stage(project,PipelineStage.ANIMATION).status,StageStatus.FAILED)
if __name__=="__main__": unittest.main()
