from dataclasses import dataclass
@dataclass
class GenerationConstraint:
    name: str
    value: str
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls, data): return cls(**data)
