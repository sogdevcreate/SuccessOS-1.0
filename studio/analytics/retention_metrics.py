from dataclasses import dataclass, field
@dataclass
class RetentionMetrics:
    average_view_duration: float | None = None; average_percentage_viewed: float | None = None
    timeline_points: list[tuple[float, float]] = field(default_factory=list); drop_off_points: list[float] = field(default_factory=list); replay_regions: list[tuple[float, float]] = field(default_factory=list)
    intro_retention: float | None = None; midpoint_retention: float | None = None; ending_retention: float | None = None
    def to_dict(self): return {"average_view_duration":self.average_view_duration,"average_percentage_viewed":self.average_percentage_viewed,"timeline_points":[list(x) for x in self.timeline_points],"drop_off_points":list(self.drop_off_points),"replay_regions":[list(x) for x in self.replay_regions],"intro_retention":self.intro_retention,"midpoint_retention":self.midpoint_retention,"ending_retention":self.ending_retention}
    @classmethod
    def from_dict(cls,d): return cls(d.get("average_view_duration"),d.get("average_percentage_viewed"),[tuple(x) for x in d.get("timeline_points",[])],list(d.get("drop_off_points",[])),[tuple(x) for x in d.get("replay_regions",[])],d.get("intro_retention"),d.get("midpoint_retention"),d.get("ending_retention"))
