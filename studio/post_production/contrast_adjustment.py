from dataclasses import dataclass
@dataclass
class ContrastAdjustment:
    amount: float = 0.0
    pivot: float = 0.5
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls,data): return cls(**data)
