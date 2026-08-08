class RenderProviderSelector:
 def __init__(self,registry):self.registry=registry
 def select(self,request):
  for provider,*_ in sorted(self.registry.enabled(),key=lambda x:x[2],reverse=True):
   caps=getattr(provider,"capabilities",{})
   if request.render_profile.codec in caps.get("codecs",set()) and request.render_profile.container in caps.get("containers",set()) and request.render_profile.fps in caps.get("fps",set()) and request.render_profile.color_space in caps.get("color_spaces",set()):return provider
  return None
