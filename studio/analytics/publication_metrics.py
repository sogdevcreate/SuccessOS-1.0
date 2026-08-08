from dataclasses import dataclass
@dataclass
class PublicationMetrics:
    impressions:int|None=None; click_through_rate:float|None=None; publication_time:str=""; processing_state:str=""; title_variant:str=""; thumbnail_variant:str=""; metadata_variant:str=""; platform_context:dict[str,str]=None
    def to_dict(self): return {**self.__dict__,"platform_context":dict(self.platform_context or {})}
    @classmethod
    def from_dict(cls,d): return cls(d.get("impressions"),d.get("click_through_rate"),str(d.get("publication_time","")),str(d.get("processing_state","")),str(d.get("title_variant","")),str(d.get("thumbnail_variant","")),str(d.get("metadata_variant","")),dict(d.get("platform_context",{})))
