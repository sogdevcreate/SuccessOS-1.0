class PublishingProviderRegistry:
 def __init__(self):self.providers={}
 def register(self,p,enabled=True,priority=0,health="healthy"):self.providers[p.identity]=(p,enabled,priority,health)
 def enabled(self):return [x for x in self.providers.values() if x[1] and x[3]=="healthy" and x[0].available()]
