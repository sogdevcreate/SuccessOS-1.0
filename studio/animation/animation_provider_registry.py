class AnimationProviderRegistry:
 def __init__(self): self.providers={}
 def register(self,provider,priority=0,quality=None): self.providers[provider.identity]=(provider,priority,quality or {})
 def enabled(self): return [value for value in self.providers.values() if value[0].available()]
