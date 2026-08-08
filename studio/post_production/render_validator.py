class RenderValidator:
 def validate(self,request,project):
  errors=[];p=request.render_profile
  if project.edit_project is None:errors.append("Approved edit is required")
  if project.color_grade is None:errors.append("Approved color grade is required")
  if not request.source_references:errors.append("Logical source media references are required")
  if p.width<=0 or p.height<=0 or p.fps<=0 or not p.codec or not p.container:errors.append("Render profile is invalid")
  if not request.output_destination:errors.append("Output destination is required")
  return errors
