from studio.enums import PipelineStage,StageStatus
from studio.pipeline.stage_result import StageResult
from studio.post_production.render_result import RenderResult,RenderResultStatus
class RenderEngine:
 def __init__(self,selector,validator,reviewer):self.selector=selector;self.validator=validator;self.reviewer=reviewer
 def __call__(self,context):
  p=context.project
  if p.render_request is None:return StageResult.failed(PipelineStage.RENDERING,"Rendering requires a populated RenderRequest")
  errors=self.validator.validate(p.render_request,p)
  if errors:return StageResult.failed(PipelineStage.RENDERING,"; ".join(errors))
  provider=self.selector.select(p.render_request)
  if provider is None:
   p.render_result=RenderResult(RenderResultStatus.UNAVAILABLE,error="No compatible render provider is configured");return StageResult.failed(PipelineStage.RENDERING,p.render_result.error)
  return StageResult.failed(PipelineStage.RENDERING,"No provider result is available; rendering remains pending")
