from dataclasses import dataclass, field


@dataclass
class VisualIdentityLock:
    reference_asset_ids: list[str] = field(default_factory=list)
    reference_handles: list[str] = field(default_factory=list)
    seed_metadata: dict[str, str] = field(default_factory=dict)
    prompt_anchors: list[str] = field(default_factory=list)
    negative_constraints: list[str] = field(default_factory=list)
    locked_appearance_attributes: dict[str, str] = field(default_factory=dict)
    provider_metadata: dict[str, dict[str, str]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {"reference_asset_ids": list(self.reference_asset_ids), "reference_handles": list(self.reference_handles), "seed_metadata": dict(self.seed_metadata), "prompt_anchors": list(self.prompt_anchors), "negative_constraints": list(self.negative_constraints), "locked_appearance_attributes": dict(self.locked_appearance_attributes), "provider_metadata": {key: dict(value) for key, value in self.provider_metadata.items()}}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "VisualIdentityLock":
        return cls(reference_asset_ids=list(data.get("reference_asset_ids", [])), reference_handles=list(data.get("reference_handles", [])), seed_metadata=dict(data.get("seed_metadata", {})), prompt_anchors=list(data.get("prompt_anchors", [])), negative_constraints=list(data.get("negative_constraints", [])), locked_appearance_attributes=dict(data.get("locked_appearance_attributes", {})), provider_metadata={key: dict(value) for key, value in data.get("provider_metadata", {}).items()})
