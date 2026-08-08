from dataclasses import dataclass, field

from studio.enums import AssetType, MediaType


@dataclass
class Asset:
    identifier: str
    asset_type: AssetType
    media_type: MediaType
    location: str
    metadata: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {"identifier": self.identifier, "asset_type": self.asset_type.value, "media_type": self.media_type.value, "location": self.location, "metadata": dict(self.metadata)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Asset":
        return cls(identifier=str(data["identifier"]), asset_type=AssetType(str(data["asset_type"])), media_type=MediaType(str(data["media_type"])), location=str(data["location"]), metadata=dict(data.get("metadata", {})))
