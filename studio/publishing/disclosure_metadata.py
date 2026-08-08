from dataclasses import dataclass,field
@dataclass
class DisclosureMetadata:
 synthetic_media:bool=False;altered_media:bool=False;sponsorship:bool=False;paid_promotion:bool=False;affiliate_relationships:bool=False;age_sensitive_material:bool=False;other_declarations:dict[str,str]=field(default_factory=dict)
 def to_dict(self): return {"synthetic_media":self.synthetic_media,"altered_media":self.altered_media,"sponsorship":self.sponsorship,"paid_promotion":self.paid_promotion,"affiliate_relationships":self.affiliate_relationships,"age_sensitive_material":self.age_sensitive_material,"other_declarations":dict(self.other_declarations)}
 @classmethod
 def from_dict(cls,data): return cls(bool(data.get("synthetic_media",False)),bool(data.get("altered_media",False)),bool(data.get("sponsorship",False)),bool(data.get("paid_promotion",False)),bool(data.get("affiliate_relationships",False)),bool(data.get("age_sensitive_material",False)),dict(data.get("other_declarations",{})))
