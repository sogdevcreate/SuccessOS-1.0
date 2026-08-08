from dataclasses import dataclass, field


@dataclass
class VisualContinuity:
    character_requirements: list[str] = field(default_factory=list)
    location_requirements: list[str] = field(default_factory=list)
    costume_requirements: list[str] = field(default_factory=list)
    prop_requirements: list[str] = field(default_factory=list)
    lighting_requirements: list[str] = field(default_factory=list)
    preserve_180_degree_rule: bool = True
    axis_of_action: str = ""

    def to_dict(self) -> dict[str, object]:
        return {"character_requirements": list(self.character_requirements), "location_requirements": list(self.location_requirements), "costume_requirements": list(self.costume_requirements), "prop_requirements": list(self.prop_requirements), "lighting_requirements": list(self.lighting_requirements), "preserve_180_degree_rule": self.preserve_180_degree_rule, "axis_of_action": self.axis_of_action}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "VisualContinuity":
        return cls(**data)
