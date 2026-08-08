from dataclasses import dataclass
@dataclass
class GenerationResult:
    provider_job_id: str
    reference_uri: str | None = None
    error: str | None = None
