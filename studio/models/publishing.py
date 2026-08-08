from dataclasses import dataclass, field


@dataclass
class PublishingMetadata:
    title: str = ""
    description: str = ""
    tags: list[str] = field(default_factory=list)
    visibility: str = "private"
    published_url: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {"title": self.title, "description": self.description, "tags": list(self.tags), "visibility": self.visibility, "published_url": self.published_url}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "PublishingMetadata":
        return cls(**data)
