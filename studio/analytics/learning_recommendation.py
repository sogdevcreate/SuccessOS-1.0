from dataclasses import dataclass, field
from enum import Enum
class RecommendationState(str,Enum): PROPOSED="proposed"; UNDER_REVIEW="under_review"; APPROVED="approved"; REJECTED="rejected"; SUPERSEDED="superseded"; DISABLED="disabled"
@dataclass
class LearningRecommendation:
    id:str; rationale:str; supporting_signal_ids:list[str]; confidence:float; expected_benefit:str; risks:list[str]; affected_subsystem:str; proposed_change:str; state:RecommendationState=RecommendationState.PROPOSED; hypothesis:str=""; causal_claim:bool=False; provenance:dict[str,str]=field(default_factory=dict)
    def to_dict(self): return {"id":self.id,"rationale":self.rationale,"supporting_signal_ids":list(self.supporting_signal_ids),"confidence":self.confidence,"expected_benefit":self.expected_benefit,"risks":list(self.risks),"affected_subsystem":self.affected_subsystem,"proposed_change":self.proposed_change,"state":self.state.value,"hypothesis":self.hypothesis,"causal_claim":self.causal_claim,"provenance":dict(self.provenance)}
    @classmethod
    def from_dict(cls,d): return cls(str(d["id"]),str(d["rationale"]),list(d.get("supporting_signal_ids",[])),float(d["confidence"]),str(d["expected_benefit"]),list(d.get("risks",[])),str(d["affected_subsystem"]),str(d["proposed_change"]),RecommendationState(str(d.get("state",RecommendationState.PROPOSED.value))),str(d.get("hypothesis","")),bool(d.get("causal_claim",False)),dict(d.get("provenance",{})))
