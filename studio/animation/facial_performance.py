from dataclasses import dataclass
@dataclass
class FacialPerformance:
    expression:str=""; emotion_intensity:float=0.; eye_direction:str=""; blinking:str=""; brow_movement:str=""; mouth_performance:str=""; micro_expressions:str=""; emotional_transitions:str=""; reaction_timing:str=""; facial_continuity:str=""
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls,d): return cls(**d)
