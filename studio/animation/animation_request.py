from dataclasses import dataclass,field
from uuid import uuid4
from studio.animation.camera_motion_plan import CameraMotionPlan
from studio.animation.facial_performance import FacialPerformance
from studio.animation.lip_sync_plan import LipSyncPlan
from studio.animation.motion_plan import MotionPlan
from studio.animation.performance_reference import PerformanceReference
from studio.animation.temporal_continuity import TemporalContinuity
@dataclass
class AnimationRequest:
    shot_id:str; scene_id:str; approved_asset_ids:list[str]; storyboard_shot_reference:str; screenplay_references:list[str]; identity_lock_bindings:list[str]; continuity_snapshot_id:str; duration_seconds:float; fps:int; resolution:str; aspect_ratio:str; motion_plan:MotionPlan=field(default_factory=MotionPlan); facial_performance:FacialPerformance=field(default_factory=FacialPerformance); lip_sync_plan:LipSyncPlan=field(default_factory=LipSyncPlan); camera_motion_plan:CameraMotionPlan=field(default_factory=CameraMotionPlan); performance_reference:PerformanceReference=field(default_factory=PerformanceReference); temporal_continuity:TemporalContinuity=field(default_factory=TemporalContinuity); audio_dialogue_timing:str=""; negative_constraints:list[str]=field(default_factory=list); quality_target:str=""; id:str=field(default_factory=lambda:str(uuid4()))
    def to_dict(self): return {"id":self.id,"shot_id":self.shot_id,"scene_id":self.scene_id,"approved_asset_ids":list(self.approved_asset_ids),"storyboard_shot_reference":self.storyboard_shot_reference,"screenplay_references":list(self.screenplay_references),"identity_lock_bindings":list(self.identity_lock_bindings),"continuity_snapshot_id":self.continuity_snapshot_id,"duration_seconds":self.duration_seconds,"fps":self.fps,"resolution":self.resolution,"aspect_ratio":self.aspect_ratio,"motion_plan":self.motion_plan.to_dict(),"facial_performance":self.facial_performance.to_dict(),"lip_sync_plan":self.lip_sync_plan.to_dict(),"camera_motion_plan":self.camera_motion_plan.to_dict(),"performance_reference":self.performance_reference.to_dict(),"temporal_continuity":self.temporal_continuity.to_dict(),"audio_dialogue_timing":self.audio_dialogue_timing,"negative_constraints":list(self.negative_constraints),"quality_target":self.quality_target}
    @classmethod
    def from_dict(cls,d):
        v=dict(d); v["motion_plan"]=MotionPlan.from_dict(v["motion_plan"]); v["facial_performance"]=FacialPerformance.from_dict(v["facial_performance"]); v["lip_sync_plan"]=LipSyncPlan.from_dict(v["lip_sync_plan"]); v["camera_motion_plan"]=CameraMotionPlan.from_dict(v["camera_motion_plan"]); v["performance_reference"]=PerformanceReference.from_dict(v["performance_reference"]); v["temporal_continuity"]=TemporalContinuity.from_dict(v["temporal_continuity"]); return cls(**v)
