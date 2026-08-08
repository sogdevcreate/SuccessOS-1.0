from dataclasses import dataclass, field

from studio.enums import PipelineStage, QualityStatus
from studio.models.quality_score import QualityScore


@dataclass
class QualityReport:
    stage: PipelineStage
    scores: list[QualityScore] = field(default_factory=list)
    threshold: float = 7.0
    reviewer_comments: list[str] = field(default_factory=list)
    improvement_suggestions: list[str] = field(default_factory=list)
    regeneration_count: int = 0
    maximum_retry_count: int = 2
    status: QualityStatus = QualityStatus.PENDING

    @property
    def overall_score(self) -> float:
        total_weight = sum(score.weight for score in self.scores)
        return sum(score.score * score.weight for score in self.scores) / total_weight if total_weight else 0.0

    @property
    def passed(self) -> bool:
        return bool(self.scores) and self.overall_score >= self.threshold

    def evaluate(self) -> QualityStatus:
        if self.passed:
            self.status = QualityStatus.PASSED
        elif self.regeneration_count >= self.maximum_retry_count:
            self.status = QualityStatus.RETRY_EXHAUSTED
        else:
            self.status = QualityStatus.FAILED
        return self.status

    def to_dict(self) -> dict[str, object]:
        return {"stage": self.stage.value, "scores": [score.to_dict() for score in self.scores], "threshold": self.threshold, "reviewer_comments": list(self.reviewer_comments), "improvement_suggestions": list(self.improvement_suggestions), "regeneration_count": self.regeneration_count, "maximum_retry_count": self.maximum_retry_count, "status": self.status.value}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "QualityReport":
        return cls(stage=PipelineStage(str(data["stage"])), scores=[QualityScore.from_dict(item) for item in data.get("scores", [])], threshold=float(data.get("threshold", 7.0)), reviewer_comments=list(data.get("reviewer_comments", [])), improvement_suggestions=list(data.get("improvement_suggestions", [])), regeneration_count=int(data.get("regeneration_count", 0)), maximum_retry_count=int(data.get("maximum_retry_count", 2)), status=QualityStatus(str(data.get("status", QualityStatus.PENDING.value))))
