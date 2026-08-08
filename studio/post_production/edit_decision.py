from dataclasses import dataclass, field
@dataclass
class EditDecision:
    id: str; kind: str; description: str; version: int = 1; references: list[str] = field(default_factory=list)
    def to_dict(self): return {"id":self.id,"kind":self.kind,"description":self.description,"version":self.version,"references":list(self.references)}
    @classmethod
    def from_dict(cls,data): return cls(**data)
