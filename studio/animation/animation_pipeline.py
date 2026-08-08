from studio.animation.animation_job import AnimationJob
class AnimationPipeline:
 def __init__(self,selector,queue,validator): self.selector=selector;self.queue=queue;self.validator=validator
 def create_job(self,request):
  errors=self.validator.validate(request)
  if errors: raise ValueError("; ".join(errors))
  provider=self.selector.select(request)
  if not provider: raise RuntimeError("No configured animation provider can satisfy the request")
  job=AnimationJob(request.id,provider.identity);self.queue.add(job);return job
