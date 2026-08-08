from dataclasses import dataclass
@dataclass
class AudioMixPlan:
 dialogue_priority:str="";narration_priority:str="";music_ducking:str="";sfx_levels:str="";ambience_levels:str="";loudness_target:str="";peak_target:str="";dynamic_range:str="";spatial_configuration:str="";mastering_intent:str=""
