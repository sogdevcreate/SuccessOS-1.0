from dataclasses import dataclass,field
@dataclass
class MusicRequest:
 cue_type:str;mood:str="";theme:str="";motif:str="";genre:str="";instrumentation:list[str]=field(default_factory=list);tempo:str="";key:str="";intensity:float=0.;start_time:float=0.;end_time:float=0.;scene_references:list[str]=field(default_factory=list)
