from dataclasses import dataclass, field
from studio.analytics.learning_recommendation import LearningRecommendation, RecommendationState
@dataclass
class OptimizationPolicy:
    id:str; recommendation_id:str; scope:str; change:str; version:int; enabled:bool=True; reversible:bool=True; provenance:dict[str,str]=field(default_factory=dict)
    @classmethod
    def from_approved_recommendation(cls, identifier, recommendation:LearningRecommendation, scope):
        if recommendation.state is not RecommendationState.APPROVED: raise ValueError("Only approved recommendations may create optimization policies")
        if not recommendation.provenance: raise ValueError("Approved recommendations require provenance")
        return cls(identifier,recommendation.id,scope,recommendation.proposed_change,1,True,True,dict(recommendation.provenance))
    def disable(self): self.enabled=False
    def to_dict(self): return {"id":self.id,"recommendation_id":self.recommendation_id,"scope":self.scope,"change":self.change,"version":self.version,"enabled":self.enabled,"reversible":self.reversible,"provenance":dict(self.provenance)}
    @classmethod
    def from_dict(cls,d): return cls(str(d["id"]),str(d["recommendation_id"]),str(d["scope"]),str(d["change"]),int(d["version"]),bool(d.get("enabled",True)),bool(d.get("reversible",True)),dict(d.get("provenance",{})))
