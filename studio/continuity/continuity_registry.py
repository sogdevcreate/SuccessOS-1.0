from dataclasses import dataclass, field

from studio.continuity.character_profile import CharacterProfile
from studio.continuity.continuity_snapshot import ContinuitySnapshot
from studio.continuity.environment_profile import EnvironmentProfile
from studio.continuity.prop_profile import PropProfile


@dataclass
class ContinuityRegistry:
    characters: dict[str, CharacterProfile] = field(default_factory=dict)
    environments: dict[str, EnvironmentProfile] = field(default_factory=dict)
    props: dict[str, PropProfile] = field(default_factory=dict)
    snapshots: list[ContinuitySnapshot] = field(default_factory=list)

    def create_snapshot(self, scene_id: str, time_progression: str = "") -> ContinuitySnapshot:
        snapshot = ContinuitySnapshot(scene_id, {key: {"age_state": value.age_progression_state, "injuries": ", ".join(value.injuries_scars_marks)} for key, value in self.characters.items()}, {key: {"location": value.current_location, "damage": value.damage_state, "owner": value.ownership} for key, value in self.props.items()}, {key: {"weather": value.weather, "time_of_day": value.time_of_day, "damage": value.environmental_damage_state} for key, value in self.environments.items()}, time_progression)
        self.snapshots.append(snapshot); return snapshot

    def restore(self, snapshot: ContinuitySnapshot) -> None:
        for key, state in snapshot.character_states.items():
            if key in self.characters:
                self.characters[key].age_progression_state = state.get("age_state", "")
                self.characters[key].injuries_scars_marks = [item for item in state.get("injuries", "").split(", ") if item]
        for key, state in snapshot.prop_states.items():
            if key in self.props:
                self.props[key].current_location = state.get("location", ""); self.props[key].damage_state = state.get("damage", ""); self.props[key].ownership = state.get("owner", "")
        for key, state in snapshot.environment_states.items():
            if key in self.environments:
                self.environments[key].weather = state.get("weather", ""); self.environments[key].time_of_day = state.get("time_of_day", ""); self.environments[key].environmental_damage_state = state.get("damage", "")

    def to_dict(self) -> dict[str, object]: return {"characters": {key: value.to_dict() for key, value in self.characters.items()}, "environments": {key: value.to_dict() for key, value in self.environments.items()}, "props": {key: value.to_dict() for key, value in self.props.items()}, "snapshots": [item.to_dict() for item in self.snapshots]}
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ContinuityRegistry": return cls(characters={key: CharacterProfile.from_dict(value) for key, value in data.get("characters", {}).items()}, environments={key: EnvironmentProfile.from_dict(value) for key, value in data.get("environments", {}).items()}, props={key: PropProfile.from_dict(value) for key, value in data.get("props", {}).items()}, snapshots=[ContinuitySnapshot.from_dict(item) for item in data.get("snapshots", [])])
