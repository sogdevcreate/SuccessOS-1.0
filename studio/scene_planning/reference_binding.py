from dataclasses import dataclass
@dataclass
class ReferenceBinding:
    reference_id: str
    kind: str
    purpose: str = ""
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls, data): return cls(**data)
