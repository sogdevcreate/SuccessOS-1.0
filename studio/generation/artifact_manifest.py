from dataclasses import dataclass, field
from studio.generation.generated_asset import GeneratedAsset
@dataclass
class ArtifactManifest:
    assets: list[GeneratedAsset] = field(default_factory=list)
    def add(self, asset): self.assets.append(asset)
    def to_dict(self): return {"assets": [asset.to_dict() for asset in self.assets]}
