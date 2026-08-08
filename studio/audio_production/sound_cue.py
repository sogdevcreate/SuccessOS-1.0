from dataclasses import dataclass
@dataclass
class SoundCue: kind:str;source_reference:str;start:float;end:float;intensity:float=0.
