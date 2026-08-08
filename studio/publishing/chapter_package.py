from dataclasses import dataclass
@dataclass
class ChapterPackage:
 title:str;start:float;end:float;scene_references:list[str]
 def valid_for(self,runtime):return 0<=self.start<=self.end<=runtime
 def to_dict(self): return {"title":self.title,"start":self.start,"end":self.end,"scene_references":list(self.scene_references)}
 @classmethod
 def from_dict(cls,data): return cls(str(data["title"]),float(data["start"]),float(data["end"]),list(data.get("scene_references",[])))
