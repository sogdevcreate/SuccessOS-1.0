from studio.enums import PipelineStage,StageStatus
from studio.pipeline.stage_result import StageResult
class AnimationEngine:
 def __init__(self,pipeline,reviewer): self.pipeline=pipeline;self.reviewer=reviewer
 def __call__(self,context):
  p=context.project
  if not p.animation_requests:return StageResult.failed(PipelineStage.ANIMATION,"No provider-ready AnimationRequests are configured")
  try:
   for request in p.animation_requests:self.pipeline.create_job(request)
  except (ValueError,RuntimeError) as error:return StageResult.failed(PipelineStage.ANIMATION,str(error))
  if not p.shot_animations:return StageResult.failed(PipelineStage.ANIMATION,"Animation jobs are queued; no animated shots are available")
  reports=[self.reviewer.review(shot,p) for shot in p.shot_animations]
  if not all(r.passed for r in reports):return StageResult.failed(PipelineStage.ANIMATION,"Animated shots did not meet the quality threshold")
  for shot,r in zip(p.shot_animations,reports):shot.quality_report=r;shot.accepted=True
  return StageResult(PipelineStage.ANIMATION,StageStatus.SUCCEEDED,quality_report=reports[0])
