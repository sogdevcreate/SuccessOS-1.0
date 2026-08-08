from dataclasses import dataclass,field
@dataclass
class RightsDeclaration:
 final_master_rights:str="";generated_asset_rights:str="";music_rights:str="";voice_rights:str="";sound_effect_rights:str="";stock_reference_rights:str="";attribution_requirements:list[str]=field(default_factory=list);commercial_use:bool=False;restrictions:list[str]=field(default_factory=list);unresolved_issues:list[str]=field(default_factory=list)
 @property
 def resolved(self):return not self.unresolved_issues and all([self.final_master_rights,self.generated_asset_rights,self.music_rights,self.voice_rights,self.sound_effect_rights])
 def to_dict(self): return {"final_master_rights":self.final_master_rights,"generated_asset_rights":self.generated_asset_rights,"music_rights":self.music_rights,"voice_rights":self.voice_rights,"sound_effect_rights":self.sound_effect_rights,"stock_reference_rights":self.stock_reference_rights,"attribution_requirements":list(self.attribution_requirements),"commercial_use":self.commercial_use,"restrictions":list(self.restrictions),"unresolved_issues":list(self.unresolved_issues)}
 @classmethod
 def from_dict(cls,data): return cls(str(data.get("final_master_rights","")),str(data.get("generated_asset_rights","")),str(data.get("music_rights","")),str(data.get("voice_rights","")),str(data.get("sound_effect_rights","")),str(data.get("stock_reference_rights","")),list(data.get("attribution_requirements",[])),bool(data.get("commercial_use",False)),list(data.get("restrictions",[])),list(data.get("unresolved_issues",[])))
