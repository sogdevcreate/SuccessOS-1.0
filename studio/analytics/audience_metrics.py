from dataclasses import dataclass, field
@dataclass
class AudienceMetrics:
    views: int | None = None; unique_viewers: int | None = None; returning_viewers: int | None = None; follower_change: int | None = None
    geography: dict[str, int] = field(default_factory=dict); languages: dict[str, int] = field(default_factory=dict); devices: dict[str, int] = field(default_factory=dict)
    privacy_scope: str = "aggregate_only"
    def to_dict(self): return {"views":self.views,"unique_viewers":self.unique_viewers,"returning_viewers":self.returning_viewers,"follower_change":self.follower_change,"geography":dict(self.geography),"languages":dict(self.languages),"devices":dict(self.devices),"privacy_scope":self.privacy_scope}
    @classmethod
    def from_dict(cls,d): return cls(d.get("views"),d.get("unique_viewers"),d.get("returning_viewers"),d.get("follower_change"),dict(d.get("geography",{})),dict(d.get("languages",{})),dict(d.get("devices",{})),str(d.get("privacy_scope","aggregate_only")))
