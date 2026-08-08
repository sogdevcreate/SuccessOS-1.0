from dataclasses import dataclass
from studio.generation.generation_request import GenerationRequest
@dataclass
class VideoGenerationRequest: request: GenerationRequest
