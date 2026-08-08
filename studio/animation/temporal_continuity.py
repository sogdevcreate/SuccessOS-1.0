from dataclasses import dataclass,field
@dataclass
class TemporalContinuity:
    character_position:dict[str,str]=field(default_factory=dict); body_pose:str=""; facial_state:str=""; wardrobe_state:str=""; prop_state:str=""; lighting_state:str=""; camera_state:str=""; environment_state:str=""; motion_direction:str=""; screen_direction:str=""; last_frame_reference:str=""; next_shot_handoff:str=""
    def to_dict(self): return {"character_position":dict(self.character_position),**{k:v for k,v in self.__dict__.items() if k!="character_position"}}
    @classmethod
    def from_dict(cls,d): return cls(**d)
