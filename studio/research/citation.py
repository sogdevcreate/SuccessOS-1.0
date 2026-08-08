from dataclasses import dataclass, field


@dataclass(frozen=True)
class Citation:
    source_id: str
    locator: str = ""
    quoted_text: str = ""
    metadata: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {"source_id": self.source_id, "locator": self.locator, "quoted_text": self.quoted_text, "metadata": dict(self.metadata)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Citation":
        return cls(source_id=str(data["source_id"]), locator=str(data.get("locator", "")), quoted_text=str(data.get("quoted_text", "")), metadata=dict(data.get("metadata", {})))
