from dataclasses import dataclass,field
@dataclass
class SynchronizationPlan:
    dialogue_references:list[str]=field(default_factory=list); narration_references:list[str]=field(default_factory=list); music_references:list[str]=field(default_factory=list); effects_references:list[str]=field(default_factory=list)
