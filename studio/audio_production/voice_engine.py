class VoiceEngine:
 def __init__(self,selector):self.selector=selector
 def submit(self,request):
  provider=self.selector.select(request)
  if not provider:raise RuntimeError("No configured voice provider is available")
  return provider.submit(request)
