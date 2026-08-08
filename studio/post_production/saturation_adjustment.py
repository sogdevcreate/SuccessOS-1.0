from dataclasses import dataclass
@dataclass
class SaturationAdjustment:
    amount: float = 0.0
    skin_tone_protection: bool = True
    skin_tone_notes: str = "Preserve photorealistic human skin tones."
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls,data): return cls(**data)
