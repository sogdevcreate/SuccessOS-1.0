from studio.enums import PipelineStage,StageStatus
from studio.pipeline.stage_result import StageResult
from studio.publishing.publish_result import PublishResult,PublishResultStatus
class PublishingEngine:
 def __init__(self,selector,validator,reviewer):self.selector=selector;self.validator=validator;self.reviewer=reviewer
 def __call__(self,context):
  p=context.project
  if p.publish_request is None:return StageResult.failed(PipelineStage.PUBLISH,"Publishing requires a populated PublishRequest")
  errors=self.validator.validate(p.publish_request,p)
  if errors:return StageResult.failed(PipelineStage.PUBLISH,"; ".join(errors))
  provider=self.selector.select(p.publish_request)
  if provider is None:
   p.publish_result=PublishResult(PublishResultStatus.UNAVAILABLE,error="No compatible publishing provider is configured");return StageResult.failed(PipelineStage.PUBLISH,p.publish_result.error)
  return StageResult.failed(PipelineStage.PUBLISH,"No provider result is available; publishing remains pending")
