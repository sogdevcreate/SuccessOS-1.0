class VoiceProviderRegistry:
 def __init__(self):self.providers={}
 def register(self,p):self.providers[p.identity]=p
