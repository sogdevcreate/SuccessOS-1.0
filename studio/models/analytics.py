from dataclasses import dataclass, field


@dataclass
class Analytics:
    views: int = 0
    watch_time_seconds: float = 0.0
    engagement_rate: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {"views": self.views, "watch_time_seconds": self.watch_time_seconds, "engagement_rate": self.engagement_rate, "metrics": dict(self.metrics)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Analytics":
        return cls(**data)
