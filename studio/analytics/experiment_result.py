from dataclasses import dataclass, field
@dataclass
class ExperimentResult:
    outcome:str; confidence:float; decision:str; metrics:dict[str,float]=field(default_factory=dict)
    def to_dict(self): return {"outcome":self.outcome,"confidence":self.confidence,"decision":self.decision,"metrics":dict(self.metrics)}
    @classmethod
    def from_dict(cls,d): return cls(str(d["outcome"]),float(d["confidence"]),str(d["decision"]),dict(d.get("metrics",{})))
