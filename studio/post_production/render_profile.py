from dataclasses import dataclass
@dataclass
class RenderProfile:
    resolution: str; width: int; height: int; aspect_ratio: str; fps: int; codec: str; container: str; video_bitrate: str=""; bitrate_mode: str=""; audio_codec: str=""; audio_bitrate: str=""; sample_rate: int=0; channel_configuration: str=""; loudness_target: str=""; peak_target: str=""; color_space: str="Rec.709"; transfer_characteristics: str="SDR"; pixel_format: str=""; subtitle_mode: str=""; quality_preset: str=""
    def to_dict(self):return self.__dict__.copy()
    @classmethod
    def from_dict(cls,data):return cls(**data)
