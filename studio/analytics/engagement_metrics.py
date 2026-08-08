from dataclasses import dataclass
@dataclass
class EngagementMetrics:
    likes:int|None=None; comments:int|None=None; shares:int|None=None; saves:int|None=None; click_through_rate:float|None=None; engagement_rate:float|None=None; conversion_signals:int|None=None
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls,d): return cls(**{key:d.get(key) for key in cls.__annotations__})
