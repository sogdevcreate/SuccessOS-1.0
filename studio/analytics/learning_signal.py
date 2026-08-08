from dataclasses import dataclass, field
@dataclass
class LearningSignal:
    id:str; source_metrics:list[str]; source_project_id:str; source_publication_reference:str; observation:str; confidence:float; sample_context:str; correlation:str=""; limitations:list[str]=field(default_factory=list); provenance:dict[str,str]=field(default_factory=dict)
    def to_dict(self): return {"id":self.id,"source_metrics":list(self.source_metrics),"source_project_id":self.source_project_id,"source_publication_reference":self.source_publication_reference,"observation":self.observation,"confidence":self.confidence,"sample_context":self.sample_context,"correlation":self.correlation,"limitations":list(self.limitations),"provenance":dict(self.provenance)}
    @classmethod
    def from_dict(cls,d): return cls(str(d["id"]),list(d.get("source_metrics",[])),str(d["source_project_id"]),str(d["source_publication_reference"]),str(d["observation"]),float(d["confidence"]),str(d["sample_context"]),str(d.get("correlation","")),list(d.get("limitations",[])),dict(d.get("provenance",{})))
