from dataclasses import dataclass,field
from studio.audio_production.audio_clip import AudioClip
@dataclass
class AudioTimeline:
 clips:list[AudioClip]=field(default_factory=list)
 def ordered(self):return sorted(self.clips,key=lambda c:c.start)
