from dataclasses import dataclass, field

from studio.storyboard.storyboard_scene import StoryboardScene


@dataclass
class CinematicStoryboard:
    title: str
    scenes: list[StoryboardScene] = field(default_factory=list)
    visual_style_target: str = "cinematic photorealism"

    @property
    def shots(self):
        return [shot for scene in self.scenes for shot in scene.sequence.ordered_shots()]

    @property
    def estimated_runtime_seconds(self) -> float:
        return sum(shot.duration_seconds for shot in self.shots)

    def to_dict(self) -> dict[str, object]:
        return {"title": self.title, "scenes": [scene.to_dict() for scene in self.scenes], "visual_style_target": self.visual_style_target}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "CinematicStoryboard":
        return cls(title=str(data["title"]), scenes=[StoryboardScene.from_dict(item) for item in data.get("scenes", [])], visual_style_target=str(data.get("visual_style_target", "cinematic photorealism")))
