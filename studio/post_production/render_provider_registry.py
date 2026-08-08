class RenderProviderRegistry:
 def __init__(self):self.records={}
 def register(self,p,enabled=True,priority=0,health="healthy",quality=None,performance=None,cost=None):self.records[p.identity]=(p,enabled,priority,health,quality or {},performance or {},cost or {})
 def enabled(self):return [x for x in self.records.values() if x[1] and x[3]=="healthy" and x[0].available()]
