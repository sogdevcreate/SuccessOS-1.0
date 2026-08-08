from dataclasses import dataclass, field
from datetime import datetime, timezone
@dataclass
class GeneratedAsset:
    id: str; asset_specification_id: str; scene_id: str; shot_ids: list[str]; asset_type: str; media_type: str; reference_uri: str | None = None; local_path: str | None = None; provider: str = ""; provider_job_id: str = ""; generation_request_id: str = ""; generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc)); resolution: str = ""; aspect_ratio: str = ""; duration_seconds: float = 0.0; fps: int = 0; seed: str = ""; model_version: str = ""; reference_bindings: list[str] = field(default_factory=list); identity_lock_bindings: list[str] = field(default_factory=list); continuity_snapshot_id: str = ""; quality_report: object | None = None; accepted: bool = False; regeneration_count: int = 0; metadata: dict[str, str] = field(default_factory=dict); provenance: dict[str, str] = field(default_factory=dict)
    def to_dict(self): return {**self.__dict__, "generated_at": self.generated_at.isoformat(), "quality_report": self.quality_report.to_dict() if self.quality_report else None}
    @classmethod
    def from_dict(cls, data):
        from datetime import datetime
        values=dict(data); values["generated_at"]=datetime.fromisoformat(values["generated_at"]); values.pop("quality_report",None); return cls(**values)
