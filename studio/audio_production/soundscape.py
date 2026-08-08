from dataclasses import dataclass,field
@dataclass
class Soundscape: cues:list[SoundCue]=field(default_factory=list)
