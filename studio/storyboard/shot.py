from dataclasses import dataclass, field

from studio.storyboard.blocking_plan import BlockingPlan
from studio.storyboard.camera_plan import CameraPlan
from studio.storyboard.composition_plan import CompositionPlan
from studio.storyboard.lighting_plan import LightingPlan
from studio.storyboard.transition_plan import TransitionPlan
from studio.storyboard.visual_continuity import VisualContinuity


@dataclass
class Shot:
    id: str
    scene_id: str
    sequence_id: str
    shot_number: int
    shot_type: str
    composition: CompositionPlan
    camera_plan: CameraPlan
    blocking: BlockingPlan = field(default_factory=BlockingPlan)
    environment_requirements: list[str] = field(default_factory=list)
    prop_requirements: list[str] = field(default_factory=list)
    lighting_plan: LightingPlan = field(default_factory=LightingPlan)
    duration_seconds: float = 0.0
    transitions: TransitionPlan = field(default_factory=TransitionPlan)
    dialogue_narration_timing: str = ""
    visual_effects_needs: list[str] = field(default_factory=list)
    continuity: VisualContinuity = field(default_factory=VisualContinuity)
    source_screenplay_references: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.shot_number < 1:
            raise ValueError("shot_number must be positive")
        if self.duration_seconds < 0:
            raise ValueError("duration_seconds cannot be negative")

    @property
    def framing(self) -> str:
        return self.composition.framing

    @property
    def camera_angle(self) -> str:
        return self.composition.camera_angle

    @property
    def camera_height(self) -> str:
        return self.composition.camera_height

    @property
    def camera_movement(self) -> str:
        return self.camera_plan.movement_path

    def to_dict(self) -> dict[str, object]:
        return {"id": self.id, "scene_id": self.scene_id, "sequence_id": self.sequence_id, "shot_number": self.shot_number, "shot_type": self.shot_type, "composition": self.composition.to_dict(), "camera_plan": self.camera_plan.to_dict(), "blocking": self.blocking.to_dict(), "environment_requirements": list(self.environment_requirements), "prop_requirements": list(self.prop_requirements), "lighting_plan": self.lighting_plan.to_dict(), "duration_seconds": self.duration_seconds, "transitions": self.transitions.to_dict(), "dialogue_narration_timing": self.dialogue_narration_timing, "visual_effects_needs": list(self.visual_effects_needs), "continuity": self.continuity.to_dict(), "source_screenplay_references": list(self.source_screenplay_references)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Shot":
        values = dict(data)
        values["composition"] = CompositionPlan.from_dict(values["composition"])
        values["camera_plan"] = CameraPlan.from_dict(values["camera_plan"])
        values["blocking"] = BlockingPlan.from_dict(values.get("blocking", {}))
        values["lighting_plan"] = LightingPlan.from_dict(values.get("lighting_plan", {}))
        values["transitions"] = TransitionPlan.from_dict(values.get("transitions", {}))
        values["continuity"] = VisualContinuity.from_dict(values.get("continuity", {}))
        return cls(**values)
