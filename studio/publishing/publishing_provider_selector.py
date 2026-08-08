class PublishingProviderSelector:
 def __init__(self,r):self.r=r
 def select(self,request):
  for p,*_ in sorted(self.r.enabled(),key=lambda x:x[2],reverse=True):
   if getattr(p,"platform",None)==request.target_platform:return p
  return None
