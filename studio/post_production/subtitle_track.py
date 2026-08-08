from dataclasses import dataclass,field
from studio.post_production.caption_cue import CaptionCue
@dataclass
class SubtitleTrack:
    cues:list[CaptionCue]=field(default_factory=list)
    def ordered(self):return sorted(self.cues,key=lambda cue:cue.start)
