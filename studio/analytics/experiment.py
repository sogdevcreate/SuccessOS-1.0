from dataclasses import dataclass, field
from studio.analytics.experiment_variant import ExperimentVariant
from studio.analytics.experiment_result import ExperimentResult
@dataclass
class Experiment:
    id:str; hypothesis:str; target_metric:str; variants:list[ExperimentVariant]=field(default_factory=list); starts_at:str=""; ends_at:str=""; sample_context:str=""; result:ExperimentResult|None=None
    def to_dict(self): return {"id":self.id,"hypothesis":self.hypothesis,"target_metric":self.target_metric,"variants":[x.to_dict() for x in self.variants],"starts_at":self.starts_at,"ends_at":self.ends_at,"sample_context":self.sample_context,"result":self.result.to_dict() if self.result else None}
    @classmethod
    def from_dict(cls,d): return cls(str(d["id"]),str(d["hypothesis"]),str(d["target_metric"]),[ExperimentVariant.from_dict(x) for x in d.get("variants",[])],str(d.get("starts_at","")),str(d.get("ends_at","")),str(d.get("sample_context","")),ExperimentResult.from_dict(d["result"]) if d.get("result") else None)
