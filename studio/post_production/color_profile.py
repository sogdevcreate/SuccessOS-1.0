from dataclasses import dataclass,field
from studio.post_production.look_profile import LookProfile
@dataclass
class ColorProfile:
    name: str
    color_space: str = "Rec.709"
    look_profile: LookProfile | None = None
    day_night_consistency: str = ""
    weather_consistency: str = ""
    lighting_continuity: str = ""
    def to_dict(self): return {"name":self.name,"color_space":self.color_space,"look_profile":self.look_profile.to_dict() if self.look_profile else None,"day_night_consistency":self.day_night_consistency,"weather_consistency":self.weather_consistency,"lighting_continuity":self.lighting_continuity}
    @classmethod
    def from_dict(cls,data):
        values=dict(data);values["look_profile"]=LookProfile.from_dict(values["look_profile"]) if values.get("look_profile") else None;return cls(**values)
