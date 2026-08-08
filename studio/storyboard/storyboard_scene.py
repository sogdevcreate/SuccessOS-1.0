from dataclasses import dataclass, field

from studio.storyboard.shot_sequence import ShotSequence


@dataclass
class StoryboardScene:
    screenplay_scene_id: str
    sequence: ShotSequence
    visual_summary: str = ""

    def to_dict(self) -> dict[str, object]:
        return {"screenplay_scene_id": self.screenplay_scene_id, "sequence": self.sequence.to_dict(), "visual_summary": self.visual_summary}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "StoryboardScene":
        return cls(screenplay_scene_id=str(data["screenplay_scene_id"]), sequence=ShotSequence.from_dict(data["sequence"]), visual_summary=str(data.get("visual_summary", "")))
