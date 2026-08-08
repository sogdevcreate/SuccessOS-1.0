from dataclasses import dataclass,field
from uuid import uuid4
from studio.audio_production.voice_performance import VoicePerformance
@dataclass
class VoiceRequest:
 performance:VoicePerformance;shot_reference:str="";quality_target:str="";id:str=field(default_factory=lambda:str(uuid4()))
 def to_dict(self):return {"id":self.id,"performance":self.performance.to_dict(),"shot_reference":self.shot_reference,"quality_target":self.quality_target}
 @classmethod
 def from_dict(cls,d):return cls(VoicePerformance.from_dict(d["performance"]),str(d.get("shot_reference","")),str(d.get("quality_target","")),str(d["id"]))
