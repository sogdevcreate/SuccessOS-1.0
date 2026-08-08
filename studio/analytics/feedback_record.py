from dataclasses import dataclass, field
@dataclass
class FeedbackRecord:
    id:str; source_type:str; source_reference:str; created_at:str; content:str; provenance:dict[str,str]=field(default_factory=dict)
    def to_dict(self): return {"id":self.id,"source_type":self.source_type,"source_reference":self.source_reference,"created_at":self.created_at,"content":self.content,"provenance":dict(self.provenance)}
    @classmethod
    def from_dict(cls,d): return cls(str(d["id"]),str(d["source_type"]),str(d["source_reference"]),str(d["created_at"]),str(d["content"]),dict(d.get("provenance",{})))
