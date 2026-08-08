from dataclasses import dataclass,field
@dataclass
class SubtitlePackage:
 language:str;asset_reference:str;timing_reference:str="";accessibility_metadata:dict[str,str]=field(default_factory=dict);forced:bool=False;default:bool=False;provenance:dict[str,str]=field(default_factory=dict)
 def to_dict(self): return {"language":self.language,"asset_reference":self.asset_reference,"timing_reference":self.timing_reference,"accessibility_metadata":dict(self.accessibility_metadata),"forced":self.forced,"default":self.default,"provenance":dict(self.provenance)}
 @classmethod
 def from_dict(cls,data): return cls(str(data["language"]),str(data["asset_reference"]),str(data.get("timing_reference","")),dict(data.get("accessibility_metadata",{})),bool(data.get("forced",False)),bool(data.get("default",False)),dict(data.get("provenance",{})))
