from dataclasses import dataclass,field
from studio.post_production.edit_decision import EditDecision
from studio.post_production.edit_timeline import EditTimeline
@dataclass
class EditProject:
    title:str;timeline:EditTimeline=field(default_factory=EditTimeline);decisions:list[EditDecision]=field(default_factory=list);synchronization_plan:object|None=None
    def to_dict(self):return {"title":self.title,"timeline":self.timeline.to_dict(),"decisions":[x.to_dict() for x in self.decisions]}
    @classmethod
    def from_dict(cls,data):return cls(str(data["title"]),EditTimeline.from_dict(data.get("timeline",{})),[EditDecision.from_dict(x) for x in data.get("decisions",[])])
