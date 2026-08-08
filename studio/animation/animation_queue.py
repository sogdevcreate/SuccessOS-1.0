class AnimationQueue:
 def __init__(self): self.jobs={}
 def add(self,job): self.jobs[job.id]=job
 def ready(self): return [j for j in self.jobs.values() if j.status.value=="queued" and all(self.jobs[d].status.value=="completed" for d in j.dependencies)]
