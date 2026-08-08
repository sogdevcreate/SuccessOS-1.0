from dataclasses import dataclass,field
from studio.post_production.exposure_adjustment import ExposureAdjustment
from studio.post_production.contrast_adjustment import ContrastAdjustment
from studio.post_production.white_balance import WhiteBalance
from studio.post_production.saturation_adjustment import SaturationAdjustment
@dataclass
class ShotGrade:
    shot_id: str
    scene_id: str
    exposure: ExposureAdjustment = field(default_factory=ExposureAdjustment)
    contrast: ContrastAdjustment = field(default_factory=ContrastAdjustment)
    white_balance: WhiteBalance = field(default_factory=WhiteBalance)
    saturation: SaturationAdjustment = field(default_factory=SaturationAdjustment)
    per_shot_overrides: dict[str,str] = field(default_factory=dict)
    provenance: dict[str,str] = field(default_factory=dict)
    def to_dict(self): return {"shot_id":self.shot_id,"scene_id":self.scene_id,"exposure":self.exposure.to_dict(),"contrast":self.contrast.to_dict(),"white_balance":self.white_balance.to_dict(),"saturation":self.saturation.to_dict(),"per_shot_overrides":dict(self.per_shot_overrides),"provenance":dict(self.provenance)}
    @classmethod
    def from_dict(cls,data):
        values=dict(data);values["exposure"]=ExposureAdjustment.from_dict(values.get("exposure",{}));values["contrast"]=ContrastAdjustment.from_dict(values.get("contrast",{}));values["white_balance"]=WhiteBalance.from_dict(values.get("white_balance",{}));values["saturation"]=SaturationAdjustment.from_dict(values.get("saturation",{}));return cls(**values)
