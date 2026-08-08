class AnalyticsProviderSelector:
    def __init__(self, registry): self._registry=registry
    def select(self, source=""):
        candidates=sorted(self._registry.enabled(),key=lambda item:item[2],reverse=True)
        return next((item[0] for item in candidates if not source or getattr(item[0],"source",None)==source),None)
