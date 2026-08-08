from dataclasses import dataclass, field
@dataclass
class CostMetrics:
    category_costs:dict[str,float]=field(default_factory=dict); total_project_cost:float|None=None; cost_per_finished_minute:float|None=None; cost_per_approved_asset:float|None=None; cost_per_regeneration:float|None=None; currency:str=""
    def to_dict(self): return {"category_costs":dict(self.category_costs),"total_project_cost":self.total_project_cost,"cost_per_finished_minute":self.cost_per_finished_minute,"cost_per_approved_asset":self.cost_per_approved_asset,"cost_per_regeneration":self.cost_per_regeneration,"currency":self.currency}
    @classmethod
    def from_dict(cls,d): return cls(dict(d.get("category_costs",{})),d.get("total_project_cost"),d.get("cost_per_finished_minute"),d.get("cost_per_approved_asset"),d.get("cost_per_regeneration"),str(d.get("currency","")))
