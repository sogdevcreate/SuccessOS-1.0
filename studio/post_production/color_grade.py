from dataclasses import dataclass,field
from studio.post_production.color_profile import ColorProfile
from studio.post_production.shot_grade import ShotGrade
from studio.post_production.shot_match_plan import ShotMatchPlan
@dataclass
class ColorGrade:
    id: str
    profile: ColorProfile
    shot_grades: list[ShotGrade] = field(default_factory=list)
    shot_match_plans: list[ShotMatchPlan] = field(default_factory=list)
    grading_decision_version: int = 1
    provenance: dict[str,str] = field(default_factory=dict)
    def to_dict(self): return {"id":self.id,"profile":self.profile.to_dict(),"shot_grades":[item.to_dict() for item in self.shot_grades],"shot_match_plans":[item.to_dict() for item in self.shot_match_plans],"grading_decision_version":self.grading_decision_version,"provenance":dict(self.provenance)}
    @classmethod
    def from_dict(cls,data): return cls(str(data["id"]),ColorProfile.from_dict(data["profile"]),[ShotGrade.from_dict(item) for item in data.get("shot_grades",[])],[ShotMatchPlan.from_dict(item) for item in data.get("shot_match_plans",[])],int(data.get("grading_decision_version",1)),dict(data.get("provenance",{})))
