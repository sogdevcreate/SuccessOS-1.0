from dataclasses import dataclass
from enum import Enum
class PublishResultStatus(str,Enum):UNAVAILABLE="unavailable";FAILED="failed";COMPLETED="completed"
@dataclass
class PublishResult:
 status:PublishResultStatus;external_id:str="";publication_reference:str="";error:str=""
 def to_dict(self): return {"status":self.status.value,"external_id":self.external_id,"publication_reference":self.publication_reference,"error":self.error}
 @classmethod
 def from_dict(cls,data): return cls(PublishResultStatus(str(data["status"])),str(data.get("external_id","")),str(data.get("publication_reference","")),str(data.get("error","")))
