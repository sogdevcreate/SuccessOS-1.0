from dataclasses import dataclass
from enum import Enum
class RenderJobStatus(str,Enum): QUEUED="queued";VALIDATING="validating";RENDERING="rendering";COMPLETED="completed";FAILED="failed";CANCELLED="cancelled";RETRYING="retrying"
@dataclass
class RenderJob: request_id:str;provider_id:str="";status:RenderJobStatus=RenderJobStatus.QUEUED;progress:float=0.;provider_job_id:str="";failure_details:str="";retry_history:list[str]=None
