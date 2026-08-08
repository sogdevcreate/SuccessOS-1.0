class PublishingQueue:
 def __init__(self):self.jobs=[]
 def add(self,j):self.jobs.append(j)
 def cancel(self,j):j.status=type(j.status).CANCELLED
