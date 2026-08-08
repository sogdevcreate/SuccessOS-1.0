from dataclasses import dataclass, field


@dataclass
class Research:
    topic: str
    summary: str = ""
    sources: list[str] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {"topic": self.topic, "summary": self.summary, "sources": list(self.sources), "findings": list(self.findings)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Research":
        return cls(**data)
