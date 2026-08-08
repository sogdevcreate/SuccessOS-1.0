from dataclasses import dataclass, field


@dataclass
class ContinuitySnapshot:
    scene_id: str
    character_states: dict[str, dict[str, str]] = field(default_factory=dict)
    prop_states: dict[str, dict[str, str]] = field(default_factory=dict)
    environment_states: dict[str, dict[str, str]] = field(default_factory=dict)
    time_progression: str = ""

    def to_dict(self) -> dict[str, object]: return {"scene_id": self.scene_id, "character_states": {key: dict(value) for key, value in self.character_states.items()}, "prop_states": {key: dict(value) for key, value in self.prop_states.items()}, "environment_states": {key: dict(value) for key, value in self.environment_states.items()}, "time_progression": self.time_progression}
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ContinuitySnapshot": return cls(scene_id=str(data["scene_id"]), character_states={key: dict(value) for key, value in data.get("character_states", {}).items()}, prop_states={key: dict(value) for key, value in data.get("prop_states", {}).items()}, environment_states={key: dict(value) for key, value in data.get("environment_states", {}).items()}, time_progression=str(data.get("time_progression", "")))
