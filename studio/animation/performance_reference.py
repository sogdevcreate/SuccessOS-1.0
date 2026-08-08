from dataclasses import dataclass,field
@dataclass
class PerformanceReference:
    asset_ids:list[str]=field(default_factory=list); reference_handles:list[str]=field(default_factory=list); seed_metadata:dict[str,str]=field(default_factory=dict)
    def to_dict(self): return {"asset_ids":list(self.asset_ids),"reference_handles":list(self.reference_handles),"seed_metadata":dict(self.seed_metadata)}
    @classmethod
    def from_dict(cls,d): return cls(**d)
