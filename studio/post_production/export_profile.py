from dataclasses import dataclass
from studio.post_production.render_profile import RenderProfile
@dataclass
class ExportProfile:
    name:str; target_platform:str; render_profile:RenderProfile|None=None
    def to_dict(self):return {"name":self.name,"target_platform":self.target_platform,"render_profile":self.render_profile.to_dict() if self.render_profile else None}
    @classmethod
    def from_dict(cls,data):
        from studio.post_production.render_profile import RenderProfile
        return cls(str(data["name"]),str(data["target_platform"]),RenderProfile.from_dict(data["render_profile"]) if data.get("render_profile") else None)
