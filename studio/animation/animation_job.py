from dataclasses import dataclass,field
from enum import Enum
from uuid import uuid4
class AnimationJobStatus(str,Enum): QUEUED="queued";RUNNING="running";COMPLETED="completed";FAILED="failed";CANCELLED="cancelled";RETRYING="retrying"
@dataclass
class AnimationJob:
 request_id:str;provider_id:str="";dependencies:list[str]=field(default_factory=list);status:AnimationJobStatus=AnimationJobStatus.QUEUED;id:str=field(default_factory=lambda:str(uuid4()));attempts:int=0
 def transition(self,status): self.status=status
