from dataclasses import dataclass, field
from studio.analytics.audience_metrics import AudienceMetrics
from studio.analytics.retention_metrics import RetentionMetrics
from studio.analytics.engagement_metrics import EngagementMetrics
from studio.analytics.publication_metrics import PublicationMetrics
from studio.analytics.quality_metrics import QualityMetrics
from studio.analytics.production_metrics import ProductionMetrics
from studio.analytics.cost_metrics import CostMetrics
@dataclass
class PerformanceSnapshot:
    id:str; publication_reference:str; collected_at:str; collection_window:str; platform:str; source:str
    audience:AudienceMetrics=field(default_factory=AudienceMetrics); retention:RetentionMetrics=field(default_factory=RetentionMetrics); engagement:EngagementMetrics=field(default_factory=EngagementMetrics); publication:PublicationMetrics=field(default_factory=PublicationMetrics); quality:QualityMetrics=field(default_factory=QualityMetrics); production:ProductionMetrics=field(default_factory=ProductionMetrics); cost:CostMetrics=field(default_factory=CostMetrics); provenance:dict[str,str]=field(default_factory=dict)
    def to_dict(self): return {"id":self.id,"publication_reference":self.publication_reference,"collected_at":self.collected_at,"collection_window":self.collection_window,"platform":self.platform,"source":self.source,"audience":self.audience.to_dict(),"retention":self.retention.to_dict(),"engagement":self.engagement.to_dict(),"publication":self.publication.to_dict(),"quality":self.quality.to_dict(),"production":self.production.to_dict(),"cost":self.cost.to_dict(),"provenance":dict(self.provenance)}
    @classmethod
    def from_dict(cls,d): return cls(str(d["id"]),str(d["publication_reference"]),str(d["collected_at"]),str(d["collection_window"]),str(d["platform"]),str(d["source"]),AudienceMetrics.from_dict(d.get("audience",{})),RetentionMetrics.from_dict(d.get("retention",{})),EngagementMetrics.from_dict(d.get("engagement",{})),PublicationMetrics.from_dict(d.get("publication",{})),QualityMetrics.from_dict(d.get("quality",{})),ProductionMetrics.from_dict(d.get("production",{})),CostMetrics.from_dict(d.get("cost",{})),dict(d.get("provenance",{})))
