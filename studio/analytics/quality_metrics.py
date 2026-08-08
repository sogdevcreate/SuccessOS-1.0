from dataclasses import dataclass, field
@dataclass
class QualityMetrics:
    stage_scores:dict[str,float]=field(default_factory=dict); report_references:list[str]=field(default_factory=list)
    def to_dict(self): return {"stage_scores":dict(self.stage_scores),"report_references":list(self.report_references)}
    @classmethod
    def from_dict(cls,d): return cls(dict(d.get("stage_scores",{})),list(d.get("report_references",[])))
