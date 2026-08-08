from dataclasses import dataclass,field
@dataclass
class FinalFilmManifest:
 project_version:str;source_assets:list[str]=field(default_factory=list);animation_references:list[str]=field(default_factory=list);audio_references:list[str]=field(default_factory=list);edit_decisions:list[str]=field(default_factory=list);color_grade_reference:str="";render_configuration:dict[str,str]=field(default_factory=dict);providers:list[str]=field(default_factory=list);licensing_metadata:dict[str,str]=field(default_factory=dict);provenance:dict[str,str]=field(default_factory=dict)
