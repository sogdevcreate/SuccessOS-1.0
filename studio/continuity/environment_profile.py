from dataclasses import dataclass, field

from studio.continuity.location_profile import LocationProfile
from studio.continuity.set_profile import SetProfile


@dataclass
class EnvironmentProfile:
    location: LocationProfile
    set_profile: SetProfile = field(default_factory=SetProfile)
    weather: str = ""
    season: str = ""
    time_of_day: str = ""
    lighting_baseline: str = ""
    recurring_props: list[str] = field(default_factory=list)
    environmental_damage_state: str = ""
    continuity_history: list[str] = field(default_factory=list)

    @property
    def identity(self) -> str: return self.location.identity
    def to_dict(self) -> dict[str, object]: return {"location": self.location.to_dict(), "set_profile": self.set_profile.to_dict(), "weather": self.weather, "season": self.season, "time_of_day": self.time_of_day, "lighting_baseline": self.lighting_baseline, "recurring_props": list(self.recurring_props), "environmental_damage_state": self.environmental_damage_state, "continuity_history": list(self.continuity_history)}
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "EnvironmentProfile": return cls(location=LocationProfile.from_dict(data["location"]), set_profile=SetProfile.from_dict(data.get("set_profile", {})), weather=str(data.get("weather", "")), season=str(data.get("season", "")), time_of_day=str(data.get("time_of_day", "")), lighting_baseline=str(data.get("lighting_baseline", "")), recurring_props=list(data.get("recurring_props", [])), environmental_damage_state=str(data.get("environmental_damage_state", "")), continuity_history=list(data.get("continuity_history", [])))
