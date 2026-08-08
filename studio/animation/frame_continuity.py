from dataclasses import dataclass
@dataclass
class FrameContinuity:
    first_frame_reference:str=""; last_frame_reference:str=""; handoff_reference:str=""
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls,d): return cls(**d)
