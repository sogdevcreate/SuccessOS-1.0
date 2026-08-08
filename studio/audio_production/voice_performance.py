from dataclasses import dataclass,field
@dataclass
class VoicePerformance:
 character_id:str;voice_identity:str;source_reference:str;language:str="";accent:str="";age_character:str="";gender_presentation:str="";emotional_state:str="";emotional_intensity:float=0.;delivery_style:str="";pace:str="";pitch_intent:str="";volume_intent:str="";pauses:list[str]=field(default_factory=list);emphasis:list[str]=field(default_factory=list);pronunciation_hints:list[str]=field(default_factory=list);breathing:str="";performance_direction:str="";timing:str="";lip_sync_constraints:list[str]=field(default_factory=list);previous_line_continuity:str=""
 def to_dict(self):return {k:(list(v) if isinstance(v,list) else v) for k,v in self.__dict__.items()}
 @classmethod
 def from_dict(cls,d):return cls(**d)
