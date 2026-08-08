from dataclasses import dataclass, field
@dataclass
class ProviderCapability:
    name: str
    supported_modalities: set[str] = field(default_factory=set)
    character_reference: bool = False
    pose_conditioning: bool = False
    depth: bool = False
    segmentation_masks: bool = False
    camera_motion: bool = False
    lip_sync: bool = False
    audio_generation: bool = False
    max_resolution: str = ""
    max_duration_seconds: float = 0.0
    supported_aspect_ratios: set[str] = field(default_factory=set)
    def to_dict(self): return {"name": self.name, "supported_modalities": sorted(self.supported_modalities), "character_reference": self.character_reference, "pose_conditioning": self.pose_conditioning, "depth": self.depth, "segmentation_masks": self.segmentation_masks, "camera_motion": self.camera_motion, "lip_sync": self.lip_sync, "audio_generation": self.audio_generation, "max_resolution": self.max_resolution, "max_duration_seconds": self.max_duration_seconds, "supported_aspect_ratios": sorted(self.supported_aspect_ratios)}
    @classmethod
    def from_dict(cls, data):
        values = dict(data); values["supported_modalities"] = set(values.get("supported_modalities", [])); values["supported_aspect_ratios"] = set(values.get("supported_aspect_ratios", [])); return cls(**values)
