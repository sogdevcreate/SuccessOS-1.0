from dataclasses import dataclass,field
@dataclass
class LipSyncPlan:
    dialogue_reference:str=""; speaker:str=""; timing:str=""; phoneme_viseme_timeline:list[str]=field(default_factory=list); mouth_shape_targets:list[str]=field(default_factory=list); language:str=""; speech_rate:float=0.; sync_tolerance:float=0.; emotion_coupling:str=""; confidence:float=0.
    def to_dict(self): return {k:(list(v) if isinstance(v,list) else v) for k,v in self.__dict__.items()}
    @classmethod
    def from_dict(cls,d): return cls(**d)
