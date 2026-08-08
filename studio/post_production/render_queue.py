class RenderQueue:
 def __init__(self):self.jobs=[]
 def add(self,job):self.jobs.append(job)
 def cancel(self,job):job.status=type(job.status).CANCELLED
