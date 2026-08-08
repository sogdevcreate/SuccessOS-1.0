from dataclasses import dataclass, field


@dataclass
class LightingPlan:
    key_light: str = ""
    fill_light: str = ""
    rim_back_light: str = ""
    practical_lights: list[str] = field(default_factory=list)
    environment_light: str = ""
    time_of_day_lighting: str = ""
    exposure_intent: str = ""
    contrast: str = ""
    shadow_character: str = ""
    color_temperature: str = ""
    mood: str = ""

    def to_dict(self) -> dict[str, object]:
        return {"key_light": self.key_light, "fill_light": self.fill_light, "rim_back_light": self.rim_back_light, "practical_lights": list(self.practical_lights), "environment_light": self.environment_light, "time_of_day_lighting": self.time_of_day_lighting, "exposure_intent": self.exposure_intent, "contrast": self.contrast, "shadow_character": self.shadow_character, "color_temperature": self.color_temperature, "mood": self.mood}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "LightingPlan":
        return cls(**data)
