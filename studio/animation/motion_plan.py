from dataclasses import dataclass, field
@dataclass
class MotionPlan:
    character_movement:list[str]=field(default_factory=list); body_pose_transitions:list[str]=field(default_factory=list); gait:str=""; gestures:list[str]=field(default_factory=list); head_movement:str=""; hand_movement:str=""; prop_interactions:list[str]=field(default_factory=list); environment_interactions:list[str]=field(default_factory=list); physical_timing:str=""; action_intensity:float=0.; motion_smoothness:str=""; motion_continuity:str=""
    def to_dict(self): return {k:(list(v) if isinstance(v,list) else v) for k,v in self.__dict__.items()}
    @classmethod
    def from_dict(cls,d): return cls(**d)
