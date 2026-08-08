from dataclasses import dataclass


@dataclass
class CharacterIdentity:
    unique_id: str
    name: str
    age_range: str = ""
    gender_presentation: str = ""
    appearance_descriptors: list[str] | None = None

    def to_dict(self) -> dict[str, object]:
        return {"unique_id": self.unique_id, "name": self.name, "age_range": self.age_range, "gender_presentation": self.gender_presentation, "appearance_descriptors": list(self.appearance_descriptors or [])}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "CharacterIdentity":
        return cls(unique_id=str(data["unique_id"]), name=str(data["name"]), age_range=str(data.get("age_range", "")), gender_presentation=str(data.get("gender_presentation", "")), appearance_descriptors=list(data.get("appearance_descriptors", [])))
