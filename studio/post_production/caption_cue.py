from dataclasses import dataclass
@dataclass
class CaptionCue:
    speaker:str;text:str;start:float;end:float;language:str="";confidence:float=0.;style_intent:str="";safe_area_position:str="";accessibility_metadata:dict|None=None
