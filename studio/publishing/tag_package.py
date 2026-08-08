from dataclasses import dataclass,field
@dataclass
class TagPackage:
 tags:list[str]=field(default_factory=list);keywords:list[str]=field(default_factory=list)
 def to_dict(self): return {"tags":list(self.tags),"keywords":list(self.keywords)}
 @classmethod
 def from_dict(cls,data): return cls(list(data.get("tags",[])),list(data.get("keywords",[])))
