from dataclasses import dataclass,field
@dataclass
class LookProfile:
    name: str
    cinematic_palette: list[str] = field(default_factory=list)
    creative_treatment: str = "photorealistic cinematic"
    directors_bible_reference: str = ""
    def to_dict(self): return {"name":self.name,"cinematic_palette":list(self.cinematic_palette),"creative_treatment":self.creative_treatment,"directors_bible_reference":self.directors_bible_reference}
    @classmethod
    def from_dict(cls,data): return cls(**data)
