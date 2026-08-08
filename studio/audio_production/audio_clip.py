from dataclasses import dataclass
@dataclass
class AudioClip:
 track:str;start:float;end:float;gain:float=0.;fade_in:float=0.;fade_out:float=0.;pan_spatial_intent:str="";source_reference:str="";scene_reference:str="";shot_reference:str=""
 @property
 def duration(self):return self.end-self.start
