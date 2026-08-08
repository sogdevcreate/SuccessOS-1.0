from dataclasses import dataclass
@dataclass
class SchedulingPlan:
 publish_immediately:bool=True;timezone:str="UTC";publication_datetime:str="";embargo:str="";premiere_intent:bool=False;platform_constraints:str=""
 def to_dict(self): return {"publish_immediately":self.publish_immediately,"timezone":self.timezone,"publication_datetime":self.publication_datetime,"embargo":self.embargo,"premiere_intent":self.premiere_intent,"platform_constraints":self.platform_constraints}
 @classmethod
 def from_dict(cls,data): return cls(bool(data.get("publish_immediately",True)),str(data.get("timezone","UTC")),str(data.get("publication_datetime","")),str(data.get("embargo","")),bool(data.get("premiere_intent",False)),str(data.get("platform_constraints","")))
