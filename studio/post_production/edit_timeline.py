from dataclasses import dataclass, field
from studio.post_production.video_track import VideoTrack
from studio.post_production.audio_track import AudioTrack
@dataclass
class EditTimeline:
    video_tracks: list[VideoTrack] = field(default_factory=list)
    audio_tracks: list[AudioTrack] = field(default_factory=list)
    subtitle_track: list[object] = field(default_factory=list)
    def ordered_video(self): return [clip for track in self.video_tracks for clip in track.ordered_clips()]
    def to_dict(self): return {"video_tracks":[x.to_dict() for x in self.video_tracks],"audio_tracks":[x.to_dict() for x in self.audio_tracks]}
    @classmethod
    def from_dict(cls,data): return cls([VideoTrack.from_dict(x) for x in data.get("video_tracks",[])],[AudioTrack.from_dict(x) for x in data.get("audio_tracks",[])])
