from dataclasses import dataclass, field
from studio.scene_planning.generation_instruction import GenerationInstruction
from studio.scene_planning.reference_binding import ReferenceBinding
@dataclass
class AssetSpecification:
    id: str
    asset_type: str
    scene_references: list[str] = field(default_factory=list)
    shot_references: list[str] = field(default_factory=list)
    source_requirements: list[str] = field(default_factory=list)
    visual_description: str = ""
    physical_material_properties: str = ""
    realism_requirements: list[str] = field(default_factory=list)
    resolution: str = ""
    aspect_ratio: str = ""
    quality_target: str = ""
    continuity_constraints: list[str] = field(default_factory=list)
    reference_bindings: list[ReferenceBinding] = field(default_factory=list)
    identity_locks: list[str] = field(default_factory=list)
    negative_constraints: list[str] = field(default_factory=list)
    generation_instruction: GenerationInstruction = field(default_factory=GenerationInstruction)
    dependencies: list[str] = field(default_factory=list)
    regeneration_rules: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    def to_dict(self): return {"id": self.id, "asset_type": self.asset_type, "scene_references": list(self.scene_references), "shot_references": list(self.shot_references), "source_requirements": list(self.source_requirements), "visual_description": self.visual_description, "physical_material_properties": self.physical_material_properties, "realism_requirements": list(self.realism_requirements), "resolution": self.resolution, "aspect_ratio": self.aspect_ratio, "quality_target": self.quality_target, "continuity_constraints": list(self.continuity_constraints), "reference_bindings": [item.to_dict() for item in self.reference_bindings], "identity_locks": list(self.identity_locks), "negative_constraints": list(self.negative_constraints), "generation_instruction": self.generation_instruction.to_dict(), "dependencies": list(self.dependencies), "regeneration_rules": list(self.regeneration_rules), "acceptance_criteria": list(self.acceptance_criteria)}
    @classmethod
    def from_dict(cls, data):
        values = dict(data); values["reference_bindings"] = [ReferenceBinding.from_dict(item) for item in values.get("reference_bindings", [])]; values["generation_instruction"] = GenerationInstruction.from_dict(values.get("generation_instruction", {})); return cls(**values)
