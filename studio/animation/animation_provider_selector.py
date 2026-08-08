class AnimationProviderSelector:
 def __init__(self,registry): self.registry=registry
 def select(self,request):
  candidates=[]
  for provider,priority,quality in self.registry.enabled():
   caps=provider.capabilities
   required={"image-to-video"}
   if request.lip_sync_plan.dialogue_reference: required.add("lip-sync")
   if not required.issubset(caps): continue
   if request.aspect_ratio not in getattr(provider,"aspect_ratios",{request.aspect_ratio}): continue
   candidates.append((priority+quality.get("photorealism",0)+quality.get("motion",0),provider))
  return max(candidates,key=lambda x:x[0])[1] if candidates else None
