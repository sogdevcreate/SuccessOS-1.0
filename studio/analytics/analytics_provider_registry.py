class AnalyticsProviderRegistry:
    def __init__(self): self._providers={}
    def register(self, provider, enabled=True, priority=0, health="healthy"): self._providers[provider.identity]=(provider,enabled,priority,health)
    def enabled(self): return [item for item in self._providers.values() if item[1] and item[3]=="healthy" and item[0].available()]
