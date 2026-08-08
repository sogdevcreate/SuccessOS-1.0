from dataclasses import dataclass

from studio.enums import PipelineStage, StageStatus
from studio.models.quality_report import QualityReport


@dataclass(frozen=True)
class StageResult:
    stage: PipelineStage
    status: StageStatus
    message: str = ""
    quality_report: QualityReport | None = None
    error: str | None = None

    @classmethod
    def failed(cls, stage: PipelineStage, error: str) -> "StageResult":
        return cls(stage=stage, status=StageStatus.FAILED, error=error)
