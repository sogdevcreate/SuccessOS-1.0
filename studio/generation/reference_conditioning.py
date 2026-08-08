from dataclasses import dataclass, field
@dataclass
class ReferenceConditioning:
    reference_images: list[str] = field(default_factory=list); character_identity: list[str] = field(default_factory=list); facial_identity: list[str] = field(default_factory=list); wardrobe_identity: list[str] = field(default_factory=list); pose: list[str] = field(default_factory=list); depth: list[str] = field(default_factory=list); masks: list[str] = field(default_factory=list); segmentation: list[str] = field(default_factory=list); environment_references: list[str] = field(default_factory=list); style_references: list[str] = field(default_factory=list); camera_references: list[str] = field(default_factory=list); previous_frame_references: list[str] = field(default_factory=list)
    def to_dict(self): return {key: list(value) for key, value in self.__dict__.items()}
    @classmethod
    def from_dict(cls, data): return cls(**data)
