from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
class JobStatus(str, Enum): QUEUED="queued"; RUNNING="running"; COMPLETED="completed"; FAILED="failed"; CANCELLED="cancelled"; RETRYING="retrying"
@dataclass
class GenerationJob:
    request_id: str; provider_id: str = ""; dependencies: list[str] = field(default_factory=list); status: JobStatus = JobStatus.QUEUED; id: str = field(default_factory=lambda: str(uuid4())); attempts: int = 0
    def transition(self, status):
        allowed={JobStatus.QUEUED:{JobStatus.RUNNING,JobStatus.CANCELLED},JobStatus.RUNNING:{JobStatus.COMPLETED,JobStatus.FAILED,JobStatus.CANCELLED},JobStatus.FAILED:{JobStatus.RETRYING},JobStatus.RETRYING:{JobStatus.RUNNING,JobStatus.CANCELLED}}
        if status not in allowed.get(self.status,set()): raise ValueError("Invalid generation job transition")
        self.status=status
