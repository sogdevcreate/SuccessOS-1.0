from dataclasses import dataclass,field
@dataclass
class DescriptionPackage:
 primary:str;short:str="";credits:list[str]=field(default_factory=list);attribution:list[str]=field(default_factory=list);chapters:list[str]=field(default_factory=list);links_metadata:dict[str,str]=field(default_factory=dict);disclosure_sections:list[str]=field(default_factory=list)
 def to_dict(self): return {"primary":self.primary,"short":self.short,"credits":list(self.credits),"attribution":list(self.attribution),"chapters":list(self.chapters),"links_metadata":dict(self.links_metadata),"disclosure_sections":list(self.disclosure_sections)}
 @classmethod
 def from_dict(cls,data): return cls(str(data["primary"]),str(data.get("short","")),list(data.get("credits",[])),list(data.get("attribution",[])),list(data.get("chapters",[])),dict(data.get("links_metadata",{})),list(data.get("disclosure_sections",[])))
