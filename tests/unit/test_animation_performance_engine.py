import unittest
from studio.animation.animation_job import AnimationJob,AnimationJobStatus
from studio.animation.animation_pipeline import AnimationPipeline
from studio.animation.animation_provider_registry import AnimationProviderRegistry
from studio.animation.animation_provider_selector import AnimationProviderSelector
from studio.animation.animation_queue import AnimationQueue
from studio.animation.animation_request import AnimationRequest
from studio.animation.animation_validator import AnimationValidator
from studio.animation.camera_motion_plan import CameraMotionPlan
from studio.animation.facial_performance import FacialPerformance
from studio.animation.lip_sync_plan import LipSyncPlan
from studio.animation.motion_plan import MotionPlan
from studio.animation.shot_assembly import ShotAssembly
from studio.enums import PipelineStage,StageStatus
class Provider:
 identity="p";capabilities={"image-to-video","lip-sync"};aspect_ratios={"16:9"}
 def available(self):return True
class AnimationTests(unittest.TestCase):
 def request(self):return AnimationRequest("shot","scene",["asset"],"board",["script"],["lock"],"snap",2,24,"4K","16:9",MotionPlan(character_movement=["walk"]),FacialPerformance(expression="fear"),LipSyncPlan(dialogue_reference="hello"),CameraMotionPlan("dolly"))
 def test_serialization_and_temporal_motion(self):
  r=AnimationRequest.from_dict(self.request().to_dict());self.assertEqual(r.motion_plan.character_movement,["walk"]);self.assertEqual(r.camera_motion_plan.movement,"dolly")
 def test_provider_selection_jobs_and_assembly(self):
  reg=AnimationProviderRegistry();reg.register(Provider(),quality={"photorealism":10,"motion":10});p=AnimationPipeline(AnimationProviderSelector(reg),AnimationQueue(),AnimationValidator());self.assertEqual(p.create_job(self.request()).provider_id,"p")
  job=AnimationJob("r");job.transition(AnimationJobStatus.RUNNING);self.assertEqual(job.status,AnimationJobStatus.RUNNING);self.assertEqual(ShotAssembly("scene",["a","b"]).ordered(),["a","b"])
 def test_missing_provider_rejected(self):
  self.assertIsNone(AnimationProviderSelector(AnimationProviderRegistry()).select(self.request()))
if __name__=="__main__":unittest.main()
