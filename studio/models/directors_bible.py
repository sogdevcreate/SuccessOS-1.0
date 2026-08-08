from dataclasses import dataclass, field


@dataclass
class DirectorsBible:
    """Production-wide creative direction and continuity rules."""

    story_vision: str = ""
    visual_rules: list[str] = field(default_factory=list)
    character_rules: list[str] = field(default_factory=list)
    camera_rules: list[str] = field(default_factory=list)
    lighting_rules: list[str] = field(default_factory=list)
    pacing_rules: list[str] = field(default_factory=list)
    editing_rules: list[str] = field(default_factory=list)
    emotion_goals: list[str] = field(default_factory=list)
    quality_targets: dict[str, float] = field(default_factory=dict)
    continuity_rules: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        for criterion, score in self.quality_targets.items():
            if not 0.0 <= score <= 10.0:
                raise ValueError(f"quality target '{criterion}' must be between 0.0 and 10.0")

    def to_dict(self) -> dict[str, object]:
        return {
            "story_vision": self.story_vision,
            "visual_rules": list(self.visual_rules),
            "character_rules": list(self.character_rules),
            "camera_rules": list(self.camera_rules),
            "lighting_rules": list(self.lighting_rules),
            "pacing_rules": list(self.pacing_rules),
            "editing_rules": list(self.editing_rules),
            "emotion_goals": list(self.emotion_goals),
            "quality_targets": dict(self.quality_targets),
            "continuity_rules": list(self.continuity_rules),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "DirectorsBible":
        return cls(**data)
