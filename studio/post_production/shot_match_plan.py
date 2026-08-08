from dataclasses import dataclass,field
@dataclass
class ShotMatchPlan:
    source_shot_id: str
    target_shot_id: str
    match_exposure: bool = True
    match_white_balance: bool = True
    match_contrast: bool = True
    match_saturation: bool = True
    skin_tone_notes: str = "Protect realistic skin tones."
    environment_color_notes: str = ""
    lighting_notes: str = ""
    time_of_day: str = ""
    weather_state: str = ""
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls,data): return cls(**data)
