class PublishingValidator:
 def validate(self,request,project):
  errors=[]
  if project.render_result is None or project.render_result.status.value!="approved":errors.append("Approved RenderResult is required")
  if not request.final_master_reference:errors.append("Final master reference is required")
  if request.rights is None or not request.rights.resolved:errors.append("Required rights information is unresolved")
  if not request.metadata.canonical_title or not request.metadata.description:errors.append("Publication metadata is incomplete")
  if request.platform_profile.max_title_length and len(request.metadata.canonical_title)>request.platform_profile.max_title_length:errors.append("Title exceeds platform limit")
  return errors
