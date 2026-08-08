from dataclasses import dataclass,field
@dataclass
class ShotAssembly:
 scene_id:str;clip_ids:list[str]=field(default_factory=list);first_frame_reference:str="";last_frame_reference:str="";dialogue_alignment:str="";camera_alignment:str=""
 def ordered(self): return list(self.clip_ids)
