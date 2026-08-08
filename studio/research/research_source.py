from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class SourceType(str, Enum):
    PRIMARY = "primary"
    ACADEMIC = "academic"
    JOURNALISM = "journalism"
    BOOK = "book"
    ARCHIVE = "archive"
    INTERVIEW = "interview"
    REFERENCE = "reference"
    OTHER = "other"


@dataclass
class ResearchSource:
    id: str
    title: str
    author: str = ""
    publisher: str = ""
    url: str = ""
    publication_date: date | None = None
    accessed_date: date | None = None
    source_type: SourceType = SourceType.OTHER
    reliability_score: float = 0.0
    relevance_score: float = 0.0
    bias_risk_notes: list[str] = field(default_factory=list)
    citation_metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, score in (("reliability_score", self.reliability_score), ("relevance_score", self.relevance_score)):
            if not 0.0 <= score <= 10.0:
                raise ValueError(f"{name} must be between 0.0 and 10.0")

    @property
    def identifier(self) -> str:
        """Compatibility alias for code using the wider Studio identifier convention."""
        return self.id

    def to_dict(self) -> dict[str, object]:
        return {"id": self.id, "title": self.title, "author": self.author, "publisher": self.publisher, "url": self.url, "publication_date": self.publication_date.isoformat() if self.publication_date else None, "accessed_date": self.accessed_date.isoformat() if self.accessed_date else None, "source_type": self.source_type.value, "reliability_score": self.reliability_score, "relevance_score": self.relevance_score, "bias_risk_notes": list(self.bias_risk_notes), "citation_metadata": dict(self.citation_metadata)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ResearchSource":
        publication_date = data.get("publication_date")
        accessed_date = data.get("accessed_date")
        source_id = data.get("id", data.get("identifier"))
        if source_id is None:
            raise ValueError("ResearchSource requires an id")
        return cls(id=str(source_id), title=str(data["title"]), author=str(data.get("author", "")), publisher=str(data.get("publisher", "")), url=str(data.get("url", "")), publication_date=date.fromisoformat(str(publication_date)) if publication_date else None, accessed_date=date.fromisoformat(str(accessed_date)) if accessed_date else None, source_type=SourceType(str(data.get("source_type", SourceType.OTHER.value))), reliability_score=float(data.get("reliability_score", 0.0)), relevance_score=float(data.get("relevance_score", 0.0)), bias_risk_notes=list(data.get("bias_risk_notes", [])), citation_metadata=dict(data.get("citation_metadata", {})))
