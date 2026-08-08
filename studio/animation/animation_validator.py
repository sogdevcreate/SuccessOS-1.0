class AnimationValidator:
 def validate(self,request):
  errors=[]
  if not request.approved_asset_ids: errors.append("Animation request lacks approved assets")
  if not request.identity_lock_bindings: errors.append("Animation request lacks identity locks")
  if not request.storyboard_shot_reference: errors.append("Animation request lacks storyboard shot")
  return errors
