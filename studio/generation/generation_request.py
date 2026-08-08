from dataclasses import dataclass, field
from uuid import uuid4
from studio.generation.reference_conditioning import ReferenceConditioning
from studio.scene_planning.asset_specification import AssetSpecification
@dataclass
class GenerationRequest:
    asset_specification: AssetSpecification
    production_profile: object
    directors_bible: object
    visual_identity_lock_bindings: list[str] = field(default_factory=list)
    continuity_registry_bindings: list[str] = field(default_factory=list)
    reference_assets: list[str] = field(default_factory=list)
    reference_conditioning: ReferenceConditioning = field(default_factory=ReferenceConditioning)
    provider_capability_requirements: set[str] = field(default_factory=set)
    deterministic_metadata: dict[str, str] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    def to_dict(self): return {"id": self.id, "asset_specification": self.asset_specification.to_dict(), "visual_identity_lock_bindings": list(self.visual_identity_lock_bindings), "continuity_registry_bindings": list(self.continuity_registry_bindings), "reference_assets": list(self.reference_assets), "reference_conditioning": self.reference_conditioning.to_dict(), "provider_capability_requirements": sorted(self.provider_capability_requirements), "deterministic_metadata": dict(self.deterministic_metadata)}
    @classmethod
    def from_dict(cls, data, profile, bible): return cls(AssetSpecification.from_dict(data["asset_specification"]), profile, bible, list(data.get("visual_identity_lock_bindings", [])), list(data.get("continuity_registry_bindings", [])), list(data.get("reference_assets", [])), ReferenceConditioning.from_dict(data.get("reference_conditioning", {})), set(data.get("provider_capability_requirements", [])), dict(data.get("deterministic_metadata", {})), str(data["id"]))
