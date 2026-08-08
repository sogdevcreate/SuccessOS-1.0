class VoiceProviderSelector:
 def __init__(self,r):self.r=r
 def select(self,request):return next((p for p in self.r.providers.values() if p.available()),None)
