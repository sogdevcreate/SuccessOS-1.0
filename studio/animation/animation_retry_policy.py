from dataclasses import dataclass
@dataclass
class AnimationRetryPolicy:
 max_retries:int=2;quality_based_regeneration:bool=True;provider_fallback:bool=True;retry_delay_seconds:float=0.
 def may_retry(self,job): return job.attempts<self.max_retries
