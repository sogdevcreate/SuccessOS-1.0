import unittest
from studio.audio_production.audio_clip import AudioClip
from studio.audio_production.audio_timeline import AudioTimeline
from studio.audio_production.voice_performance import VoicePerformance
from studio.audio_production.voice_request import VoiceRequest
class AudioProductionTests(unittest.TestCase):
 def test_voice_and_timeline(self):
  request=VoiceRequest(VoicePerformance("maya","voice","line",pronunciation_hints=["Lagos"],lip_sync_constraints=["24fps"]));self.assertEqual(VoiceRequest.from_dict(request.to_dict()).performance.character_id,"maya")
  self.assertEqual(AudioTimeline([AudioClip("dialogue",2,3),AudioClip("music",0,2)]).ordered()[0].track,"music")
if __name__=="__main__":unittest.main()
