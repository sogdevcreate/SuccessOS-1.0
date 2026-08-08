from dataclasses import dataclass, field
@dataclass
class ProductionMetrics:
    stage_durations:dict[str,float]=field(default_factory=dict); retries:dict[str,int]=field(default_factory=dict); regeneration_counts:dict[str,int]=field(default_factory=dict); failed_quality_gates:dict[str,int]=field(default_factory=dict); provider_failures:dict[str,int]=field(default_factory=dict); fallback_frequency:int|None=None; asset_rejection_rate:float|None=None; animation_rejection_rate:float|None=None; audio_rejection_rate:float|None=None; render_failures:int|None=None; publishing_failures:int|None=None
    def to_dict(self): return {key:(dict(value) if isinstance(value,dict) else value) for key,value in self.__dict__.items()}
    @classmethod
    def from_dict(cls,d): return cls(**{key:(dict(d.get(key,{})) if key in {"stage_durations","retries","regeneration_counts","failed_quality_gates","provider_failures"} else d.get(key)) for key in cls.__annotations__})
