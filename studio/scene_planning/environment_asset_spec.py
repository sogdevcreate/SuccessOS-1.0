from dataclasses import dataclass
from studio.scene_planning.asset_specification import AssetSpecification
@dataclass
class EnvironmentAssetSpec:
    specification: AssetSpecification
    environment_id: str
    location_binding: str
    set_binding: str
    weather: str
    time_of_day: str
    lighting_baseline: str
    continuity_state: str
    def to_dict(self): return {"specification": self.specification.to_dict(), **{key: value for key, value in self.__dict__.items() if key != "specification"}}
    @classmethod
    def from_dict(cls, data): return cls(AssetSpecification.from_dict(data["specification"]), *[str(data[key]) for key in ("environment_id", "location_binding", "set_binding", "weather", "time_of_day", "lighting_baseline", "continuity_state")])
