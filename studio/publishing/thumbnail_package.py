from dataclasses import dataclass,field
@dataclass
class ThumbnailPackage:
 asset_reference:str="";alternate_candidates:list[str]=field(default_factory=list);aspect_ratio:str="";resolution:str="";safe_areas:list[str]=field(default_factory=list);text_overlays:list[str]=field(default_factory=list);visual_focus:str="";character_references:list[str]=field(default_factory=list);branding:str="";selected_candidate:str="";provenance:dict[str,str]=field(default_factory=dict)
 def to_dict(self): return {"asset_reference":self.asset_reference,"alternate_candidates":list(self.alternate_candidates),"aspect_ratio":self.aspect_ratio,"resolution":self.resolution,"safe_areas":list(self.safe_areas),"text_overlays":list(self.text_overlays),"visual_focus":self.visual_focus,"character_references":list(self.character_references),"branding":self.branding,"selected_candidate":self.selected_candidate,"provenance":dict(self.provenance)}
 @classmethod
 def from_dict(cls,data): return cls(str(data.get("asset_reference","")),list(data.get("alternate_candidates",[])),str(data.get("aspect_ratio","")),str(data.get("resolution","")),list(data.get("safe_areas",[])),list(data.get("text_overlays",[])),str(data.get("visual_focus","")),list(data.get("character_references",[])),str(data.get("branding","")),str(data.get("selected_candidate","")),dict(data.get("provenance",{})))
