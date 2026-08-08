from dataclasses import dataclass, field
from studio.post_production.transition import Transition


@dataclass
class TimelineClip:
    id: str
    source_asset: str
    source_shot: str
    scene_id: str
    track_id: str
    source_in: float
    source_out: float
    timeline_in: float
    timeline_out: float
    playback_rate: float = 1.0
    transition_in: Transition = field(default_factory=Transition)
    transition_out: Transition = field(default_factory=Transition)
    synchronization_references: list[str] = field(default_factory=list)
    continuity_references: list[str] = field(default_factory=list)
    provenance: dict[str, str] = field(default_factory=dict)

    @property
    def duration(self) -> float: return self.timeline_out - self.timeline_in
    def trim(self, source_in: float, source_out: float) -> None:
        if source_out < source_in: raise ValueError("Trim out cannot precede trim in")
        self.source_in, self.source_out = source_in, source_out
    def retime(self, playback_rate: float) -> None:
        if playback_rate <= 0: raise ValueError("Playback rate must be positive")
        self.playback_rate = playback_rate
    def to_dict(self) -> dict[str, object]:
        return {"id":self.id,"source_asset":self.source_asset,"source_shot":self.source_shot,"scene_id":self.scene_id,"track_id":self.track_id,"source_in":self.source_in,"source_out":self.source_out,"timeline_in":self.timeline_in,"timeline_out":self.timeline_out,"playback_rate":self.playback_rate,"transition_in":self.transition_in.to_dict(),"transition_out":self.transition_out.to_dict(),"synchronization_references":list(self.synchronization_references),"continuity_references":list(self.continuity_references),"provenance":dict(self.provenance)}
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "TimelineClip":
        values=dict(data); values["transition_in"]=Transition.from_dict(values.get("transition_in",{})); values["transition_out"]=Transition.from_dict(values.get("transition_out",{})); return cls(**values)
