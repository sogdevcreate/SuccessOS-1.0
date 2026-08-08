from dataclasses import dataclass, field
from enum import Enum


class VerificationStatus(str, Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    DISPUTED = "disputed"


@dataclass
class Fact:
    identifier: str
    statement: str
    source_references: list[str] = field(default_factory=list)
    confidence: float = 0.0
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    disputed: bool = False
    contradiction_references: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if self.verification_status is VerificationStatus.DISPUTED:
            self.disputed = True

    def to_dict(self) -> dict[str, object]:
        return {"identifier": self.identifier, "statement": self.statement, "source_references": list(self.source_references), "confidence": self.confidence, "verification_status": self.verification_status.value, "disputed": self.disputed, "contradiction_references": list(self.contradiction_references)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Fact":
        return cls(identifier=str(data["identifier"]), statement=str(data["statement"]), source_references=list(data.get("source_references", [])), confidence=float(data.get("confidence", 0.0)), verification_status=VerificationStatus(str(data.get("verification_status", VerificationStatus.UNVERIFIED.value))), disputed=bool(data.get("disputed", False)), contradiction_references=list(data.get("contradiction_references", [])))
