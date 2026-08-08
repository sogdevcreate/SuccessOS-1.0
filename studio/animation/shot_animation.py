from dataclasses import dataclass,field
from datetime import datetime,timezone
@dataclass
class ShotAnimation:
    id:str; request_id:str; shot_id:str; provider:str=""; provider_job_id:str=""; reference_uri:str=""; accepted:bool=False; quality_report:object|None=None; regeneration_count:int=0; provenance:dict[str,str]=field(default_factory=dict); generated_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    def to_dict(self): return {**self.__dict__,"generated_at":self.generated_at.isoformat(),"quality_report":self.quality_report.to_dict() if self.quality_report else None}
