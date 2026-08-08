from dataclasses import dataclass
@dataclass
class WhiteBalance:
    temperature_kelvin: float = 6500.0
    tint: float = 0.0
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls,data): return cls(**data)
