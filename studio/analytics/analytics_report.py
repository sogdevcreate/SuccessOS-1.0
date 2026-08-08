from dataclasses import dataclass, field
from studio.analytics.performance_snapshot import PerformanceSnapshot
@dataclass
class AnalyticsReport:
    id:str; project_id:str; publication_reference:str; snapshots:list[PerformanceSnapshot]=field(default_factory=list); observations:list[str]=field(default_factory=list); unavailable:bool=False; errors:list[str]=field(default_factory=list); provenance:dict[str,str]=field(default_factory=dict)
    def to_dict(self): return {"id":self.id,"project_id":self.project_id,"publication_reference":self.publication_reference,"snapshots":[x.to_dict() for x in self.snapshots],"observations":list(self.observations),"unavailable":self.unavailable,"errors":list(self.errors),"provenance":dict(self.provenance)}
    @classmethod
    def from_dict(cls,d): return cls(str(d["id"]),str(d["project_id"]),str(d["publication_reference"]),[PerformanceSnapshot.from_dict(x) for x in d.get("snapshots",[])],list(d.get("observations",[])),bool(d.get("unavailable",False)),list(d.get("errors",[])),dict(d.get("provenance",{})))
