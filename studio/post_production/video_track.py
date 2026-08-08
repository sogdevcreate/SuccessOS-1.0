from dataclasses import dataclass, field
from studio.post_production.timeline_clip import TimelineClip
@dataclass
class VideoTrack:
    id: str
    clips: list[TimelineClip] = field(default_factory=list)
    def ordered_clips(self) -> list[TimelineClip]: return sorted(self.clips,key=lambda clip:clip.timeline_in)
    def to_dict(self): return {"id":self.id,"clips":[clip.to_dict() for clip in self.clips]}
    @classmethod
    def from_dict(cls,data): return cls(str(data["id"]),[TimelineClip.from_dict(item) for item in data.get("clips",[])])
