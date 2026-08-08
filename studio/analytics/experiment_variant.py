from dataclasses import dataclass, field
@dataclass
class ExperimentVariant:
    id:str; name:str; changes:dict[str,str]=field(default_factory=dict); control:bool=False
    def to_dict(self): return {"id":self.id,"name":self.name,"changes":dict(self.changes),"control":self.control}
    @classmethod
    def from_dict(cls,d): return cls(str(d["id"]),str(d["name"]),dict(d.get("changes",{})),bool(d.get("control",False)))
