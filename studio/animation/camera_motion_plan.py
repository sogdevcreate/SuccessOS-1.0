from dataclasses import dataclass
@dataclass
class CameraMotionPlan:
    movement:str="static"; rack_focus_timing:str=""; path:str=""; target:str=""; speed:str=""; easing:str=""; stabilization:str=""; adjacent_shot_continuity:str=""
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls,d): return cls(**d)
