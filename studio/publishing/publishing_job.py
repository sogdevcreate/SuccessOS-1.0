from dataclasses import dataclass
from enum import Enum
class PublishingJobStatus(str,Enum):QUEUED="queued";VALIDATING="validating";WAITING_FOR_SCHEDULE="waiting_for_schedule";PUBLISHING="publishing";PROCESSING="processing";COMPLETED="completed";FAILED="failed";CANCELLED="cancelled";UNAVAILABLE="unavailable"
@dataclass
class PublishingJob:request_id:str;status:PublishingJobStatus=PublishingJobStatus.QUEUED;provider_id:str="";progress:float=0.;external_id:str="";failure_information:str="";retries:int=0
