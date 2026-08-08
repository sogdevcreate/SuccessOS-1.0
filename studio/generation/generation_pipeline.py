from studio.generation.generation_job import GenerationJob
class GenerationPipeline:
    def __init__(self, selector, queue, validator): self._selector=selector; self._queue=queue; self._validator=validator
    def create_job(self, request):
        errors=self._validator.validate(request)
        if errors: raise ValueError("; ".join(errors))
        provider=self._selector.select(request)
        if provider is None: raise RuntimeError("No configured provider can satisfy the generation request")
        job=GenerationJob(request.id, provider.identity, list(request.asset_specification.dependencies)); self._queue.add(job); return job
