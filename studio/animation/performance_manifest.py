from dataclasses import dataclass,field
@dataclass
class PerformanceManifest:
 shots:list[object]=field(default_factory=list)
