from dataclasses import dataclass, field

from studio.screenwriting.character_arc import CharacterArc
from studio.screenwriting.screenplay_scene import ScreenplayScene
from studio.screenwriting.story_structure import StoryStructure


@dataclass
class Screenplay:
    title: str
    logline: str = ""
    premise: str = ""
    genre: str = ""
    tone: str = ""
    target_audience: str = ""
    hook: str = ""
    opening_sequence: str = ""
    story_structure: StoryStructure = field(default_factory=StoryStructure)
    scenes: list[ScreenplayScene] = field(default_factory=list)
    character_arcs: list[CharacterArc] = field(default_factory=list)
    emotional_arcs: list[str] = field(default_factory=list)
    pacing_notes: list[str] = field(default_factory=list)
    tension_curve: list[float] = field(default_factory=list)
    callbacks: list[str] = field(default_factory=list)
    reveals: list[str] = field(default_factory=list)
    call_to_action: str = ""

    def __post_init__(self) -> None:
        if any(not 0.0 <= value <= 10.0 for value in self.tension_curve):
            raise ValueError("tension_curve values must be between 0.0 and 10.0")

    @property
    def sequences(self) -> list[str]:
        return self.story_structure.sequences

    @property
    def climax(self) -> str:
        return self.story_structure.climax

    @property
    def resolution(self) -> str:
        return self.story_structure.resolution

    @property
    def estimated_runtime_seconds(self) -> float:
        return sum(scene.duration_seconds for scene in self.ordered_scenes())

    def ordered_scenes(self) -> list[ScreenplayScene]:
        return sorted(self.scenes, key=lambda scene: scene.scene_number)

    def to_dict(self) -> dict[str, object]:
        return {"title": self.title, "logline": self.logline, "premise": self.premise, "genre": self.genre, "tone": self.tone, "target_audience": self.target_audience, "hook": self.hook, "opening_sequence": self.opening_sequence, "story_structure": self.story_structure.to_dict(), "scenes": [scene.to_dict() for scene in self.scenes], "character_arcs": [arc.to_dict() for arc in self.character_arcs], "emotional_arcs": list(self.emotional_arcs), "pacing_notes": list(self.pacing_notes), "tension_curve": list(self.tension_curve), "callbacks": list(self.callbacks), "reveals": list(self.reveals), "call_to_action": self.call_to_action}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Screenplay":
        values = dict(data)
        values["story_structure"] = StoryStructure.from_dict(values.get("story_structure", {}))
        values["scenes"] = [ScreenplayScene.from_dict(item) for item in values.get("scenes", [])]
        values["character_arcs"] = [CharacterArc.from_dict(item) for item in values.get("character_arcs", [])]
        return cls(**values)
