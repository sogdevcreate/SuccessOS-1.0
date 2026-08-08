from dataclasses import dataclass, field
@dataclass
class GenerationInstruction:
    modalities: list[str] = field(default_factory=list)
    prompt: str = ""
    negative_prompt: str = ""
    character_reference_conditioning: bool = False
    camera_motion_conditioning: bool = False
    depth_input: bool = False
    mask_input: bool = False
    seed_reuse: bool = False
    quality_preset: str = ""
    frame_count: int = 0
    duration_seconds: float = 0.0
    fps: int = 0
    resolution: str = ""
    aspect_ratio: str = ""
    def to_dict(self): return {"modalities": list(self.modalities), "prompt": self.prompt, "negative_prompt": self.negative_prompt, "character_reference_conditioning": self.character_reference_conditioning, "camera_motion_conditioning": self.camera_motion_conditioning, "depth_input": self.depth_input, "mask_input": self.mask_input, "seed_reuse": self.seed_reuse, "quality_preset": self.quality_preset, "frame_count": self.frame_count, "duration_seconds": self.duration_seconds, "fps": self.fps, "resolution": self.resolution, "aspect_ratio": self.aspect_ratio}
    @classmethod
    def from_dict(cls, data): return cls(**data)
