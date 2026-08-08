from dataclasses import dataclass,field
@dataclass
class TitleCandidate:
 text:str;intended_audience:str="";hook:str="";keywords:list[str]=field(default_factory=list);score:float=0.;selected:bool=False
 def to_dict(self): return {"text":self.text,"intended_audience":self.intended_audience,"hook":self.hook,"keywords":list(self.keywords),"score":self.score,"selected":self.selected}
 @classmethod
 def from_dict(cls,data): return cls(str(data["text"]),str(data.get("intended_audience","")),str(data.get("hook","")),list(data.get("keywords",[])),float(data.get("score",0.0)),bool(data.get("selected",False)))
@dataclass
class TitlePackage:
 candidates:list[TitleCandidate]=field(default_factory=list)
 def selected(self):return next((x for x in self.candidates if x.selected),None)
 def to_dict(self): return {"candidates":[candidate.to_dict() for candidate in self.candidates]}
 @classmethod
 def from_dict(cls,data): return cls([TitleCandidate.from_dict(item) for item in data.get("candidates",[])])
