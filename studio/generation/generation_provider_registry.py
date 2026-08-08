from dataclasses import dataclass
@dataclass
class ProviderRecord:
    provider: object; enabled: bool = True; priority: int = 0; health_state: str = "healthy"; cost_metadata: dict | None = None; quality_metadata: dict | None = None
class GenerationProviderRegistry:
    def __init__(self): self._records = {}
    def register(self, record): self._records[record.provider.identity] = record
    def enabled(self): return [record for record in self._records.values() if record.enabled and record.health_state == "healthy" and record.provider.available()]
    def set_enabled(self, identity, enabled): self._records[identity].enabled = enabled
