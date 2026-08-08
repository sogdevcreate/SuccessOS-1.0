from dataclasses import dataclass, field

from studio.storyboard.shot import Shot


@dataclass
class ShotSequence:
    id: str
    scene_id: str
    shots: list[Shot] = field(default_factory=list)

    def ordered_shots(self) -> list[Shot]:
        return sorted(self.shots, key=lambda shot: shot.shot_number)

    def to_dict(self) -> dict[str, object]:
        return {"id": self.id, "scene_id": self.scene_id, "shots": [shot.to_dict() for shot in self.shots]}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ShotSequence":
        return cls(id=str(data["id"]), scene_id=str(data["scene_id"]), shots=[Shot.from_dict(item) for item in data.get("shots", [])])
