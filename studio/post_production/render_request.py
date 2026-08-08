from dataclasses import dataclass,field
from uuid import uuid4
from studio.post_production.render_profile import RenderProfile
from studio.post_production.export_profile import ExportProfile
@dataclass
class RenderRequest:
    project_id:str; project_version:str; render_profile:RenderProfile; export_profile:ExportProfile; output_destination:str; subtitle_configuration:dict[str,str]=field(default_factory=dict); source_references:list[str]=field(default_factory=list); provenance_references:list[str]=field(default_factory=list); quality_target:str=""; id:str=field(default_factory=lambda:str(uuid4()))
    def to_dict(self):return {"id":self.id,"project_id":self.project_id,"project_version":self.project_version,"render_profile":self.render_profile.to_dict(),"export_profile":self.export_profile.to_dict(),"output_destination":self.output_destination,"subtitle_configuration":dict(self.subtitle_configuration),"source_references":list(self.source_references),"provenance_references":list(self.provenance_references),"quality_target":self.quality_target}
    @classmethod
    def from_dict(cls,data):return cls(str(data["project_id"]),str(data["project_version"]),RenderProfile.from_dict(data["render_profile"]),ExportProfile.from_dict(data["export_profile"]),str(data["output_destination"]),dict(data.get("subtitle_configuration",{})),list(data.get("source_references",[])),list(data.get("provenance_references",[])),str(data.get("quality_target", "")),str(data["id"]))
