from dataclasses import dataclass
from enum import Enum
class RenderResultStatus(str,Enum): UNAVAILABLE="unavailable";FAILED="failed";REJECTED="rejected";APPROVED="approved"
@dataclass
class RenderResult:
 status:RenderResultStatus;provider_job_id:str="";reference_uri:str="";error:str=""
 def to_dict(self):return {"status":self.status.value,"provider_job_id":self.provider_job_id,"reference_uri":self.reference_uri,"error":self.error}
 @classmethod
 def from_dict(cls,data):return cls(RenderResultStatus(str(data["status"])),str(data.get("provider_job_id", "")),str(data.get("reference_uri", "")),str(data.get("error", "")))
