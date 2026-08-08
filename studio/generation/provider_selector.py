from studio.generation.provider_score import ProviderScore
from studio.scene_planning.asset_spec_validator import AssetSpecValidator
class ProviderSelector:
    def __init__(self, registry, validator=None): self._registry = registry; self._validator = validator or AssetSpecValidator()
    def select(self, request):
        candidates=[]
        for record in self._registry.enabled():
            if self._validator.validate_provider(request.asset_specification, record.provider.capabilities): continue
            if set(request.provider_capability_requirements) - record.provider.capabilities.supported_modalities: continue
            quality=(record.quality_metadata or {}).get("photorealism", 0); reliability=(record.quality_metadata or {}).get("reliability", 0); cost=(record.cost_metadata or {}).get("cost", 0)
            candidates.append((quality + reliability + record.priority - cost, record))
        if not candidates: return None
        return max(candidates, key=lambda item: item[0])[1].provider
    def score(self, request):
        provider=self.select(request); return ProviderScore(provider.identity, 0.0) if provider else None
