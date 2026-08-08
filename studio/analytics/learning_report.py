from dataclasses import dataclass, field
from studio.analytics.learning_signal import LearningSignal
from studio.analytics.learning_recommendation import LearningRecommendation
@dataclass
class LearningReport:
    id:str; analytics_report_id:str; observations:list[str]=field(default_factory=list); patterns:list[str]=field(default_factory=list); correlations:list[str]=field(default_factory=list); hypotheses:list[str]=field(default_factory=list); signals:list[LearningSignal]=field(default_factory=list); recommendations:list[LearningRecommendation]=field(default_factory=list); provenance:dict[str,str]=field(default_factory=dict)
    def to_dict(self): return {"id":self.id,"analytics_report_id":self.analytics_report_id,"observations":list(self.observations),"patterns":list(self.patterns),"correlations":list(self.correlations),"hypotheses":list(self.hypotheses),"signals":[x.to_dict() for x in self.signals],"recommendations":[x.to_dict() for x in self.recommendations],"provenance":dict(self.provenance)}
    @classmethod
    def from_dict(cls,d): return cls(str(d["id"]),str(d["analytics_report_id"]),list(d.get("observations",[])),list(d.get("patterns",[])),list(d.get("correlations",[])),list(d.get("hypotheses",[])),[LearningSignal.from_dict(x) for x in d.get("signals",[])],[LearningRecommendation.from_dict(x) for x in d.get("recommendations",[])],dict(d.get("provenance",{})))
