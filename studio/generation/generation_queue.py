class GenerationQueue:
    def __init__(self): self.jobs={}
    def add(self, job): self.jobs[job.id]=job
    def ready(self): return [job for job in self.jobs.values() if job.status.value=="queued" and all(self.jobs[dep].status.value=="completed" for dep in job.dependencies)]
    def cancel(self, job_id): self.jobs[job_id].transition(type(self.jobs[job_id].status).CANCELLED)
