from dataclasses import dataclass, field

from studio.screenwriting.dialogue_line import DialogueLine
from studio.screenwriting.narration_block import NarrationBlock
from studio.screenwriting.screenplay_beat import ScreenplayBeat


@dataclass
class ScreenplayScene:
    id: str
    scene_number: int
    slugline: str
    location: str
    time_of_day: str
    duration_seconds: float
    participating_characters: list[str] = field(default_factory=list)
    dramatic_purpose: str = ""
    visual_objective: str = ""
    emotional_objective: str = ""
    action_description: str = ""
    dialogue: list[DialogueLine] = field(default_factory=list)
    narration: list[NarrationBlock] = field(default_factory=list)
    transitions: list[str] = field(default_factory=list)
    fact_references: list[str] = field(default_factory=list)
    unsupported_claims: list[str] = field(default_factory=list)
    disputed_fact_references: list[str] = field(default_factory=list)
    continuity_requirements: list[str] = field(default_factory=list)
    directors_bible_constraints: list[str] = field(default_factory=list)
    beats: list[ScreenplayBeat] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.scene_number < 1:
            raise ValueError("scene_number must be positive")
        if self.duration_seconds < 0:
            raise ValueError("duration_seconds cannot be negative")

    @property
    def identifier(self) -> str:
        return self.id

    def to_dict(self) -> dict[str, object]:
        return {"id": self.id, "scene_number": self.scene_number, "slugline": self.slugline, "location": self.location, "time_of_day": self.time_of_day, "duration_seconds": self.duration_seconds, "participating_characters": list(self.participating_characters), "dramatic_purpose": self.dramatic_purpose, "visual_objective": self.visual_objective, "emotional_objective": self.emotional_objective, "action_description": self.action_description, "dialogue": [line.to_dict() for line in self.dialogue], "narration": [block.to_dict() for block in self.narration], "transitions": list(self.transitions), "fact_references": list(self.fact_references), "unsupported_claims": list(self.unsupported_claims), "disputed_fact_references": list(self.disputed_fact_references), "continuity_requirements": list(self.continuity_requirements), "directors_bible_constraints": list(self.directors_bible_constraints), "beats": [beat.to_dict() for beat in self.beats]}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ScreenplayScene":
        scene_id = data.get("id", data.get("identifier"))
        if scene_id is None:
            raise ValueError("ScreenplayScene requires an id")
        values = dict(data)
        values["id"] = str(scene_id)
        values.pop("identifier", None)
        values["dialogue"] = [DialogueLine.from_dict(item) for item in values.get("dialogue", [])]
        values["narration"] = [NarrationBlock.from_dict(item) for item in values.get("narration", [])]
        values["beats"] = [ScreenplayBeat.from_dict(item) for item in values.get("beats", [])]
        return cls(**values)
