from dataclasses import dataclass, field
from studio.scene_planning.scene_requirement import SceneRequirement
@dataclass
class ScenePlan:
    scene_id: str
    screenplay_scene_id: str
    storyboard_scene_id: str
    duration_seconds: float
    location: str = ""
    time_of_day: str = ""
    weather: str = ""
    participating_characters: list[str] = field(default_factory=list)
    wardrobe_state: list[str] = field(default_factory=list)
    props: list[str] = field(default_factory=list)
    environment_state: list[str] = field(default_factory=list)
    lighting_intent: str = ""
    camera_shot_references: list[str] = field(default_factory=list)
    dialogue_timing: str = ""
    narration_timing: str = ""
    sound_requirements: list[str] = field(default_factory=list)
    vfx_requirements: list[str] = field(default_factory=list)
    continuity_bindings: list[str] = field(default_factory=list)
    required_assets: list[str] = field(default_factory=list)
    generation_order: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    production_risks: list[str] = field(default_factory=list)
    requirements: list[SceneRequirement] = field(default_factory=list)
    def to_dict(self): return {"scene_id": self.scene_id, "screenplay_scene_id": self.screenplay_scene_id, "storyboard_scene_id": self.storyboard_scene_id, "duration_seconds": self.duration_seconds, "location": self.location, "time_of_day": self.time_of_day, "weather": self.weather, "participating_characters": list(self.participating_characters), "wardrobe_state": list(self.wardrobe_state), "props": list(self.props), "environment_state": list(self.environment_state), "lighting_intent": self.lighting_intent, "camera_shot_references": list(self.camera_shot_references), "dialogue_timing": self.dialogue_timing, "narration_timing": self.narration_timing, "sound_requirements": list(self.sound_requirements), "vfx_requirements": list(self.vfx_requirements), "continuity_bindings": list(self.continuity_bindings), "required_assets": list(self.required_assets), "generation_order": list(self.generation_order), "dependencies": list(self.dependencies), "production_risks": list(self.production_risks), "requirements": [item.to_dict() for item in self.requirements]}
    @classmethod
    def from_dict(cls, data):
        values = dict(data); values["requirements"] = [SceneRequirement.from_dict(item) for item in values.get("requirements", [])]; return cls(**values)
