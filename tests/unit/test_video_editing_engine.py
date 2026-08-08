import unittest
from studio.post_production.edit_decision import EditDecision
from studio.post_production.edit_project import EditProject
from studio.post_production.edit_quality_reviewer import EditQualityReviewer
from studio.post_production.edit_timeline import EditTimeline
from studio.post_production.timeline_clip import TimelineClip
from studio.post_production.transition import Transition
from studio.post_production.video_track import VideoTrack
from studio.post_production.subtitle_track import SubtitleTrack
from studio.post_production.caption_cue import CaptionCue
class VideoEditingTests(unittest.TestCase):
 def test_timeline_clip_editing_and_serialization(self):
  clip=TimelineClip("c","asset","shot","scene","v1",0,4,2,6,transition_in=Transition("j-cut",.2));clip.trim(1,3);clip.retime(1.25);self.assertEqual(TimelineClip.from_dict(clip.to_dict()).playback_rate,1.25)
 def test_ordering_subtitles_and_quality(self):
  edit=EditProject("Film",EditTimeline([VideoTrack("v",[TimelineClip("b","a","s","2","v",0,1,3,4),TimelineClip("a","a","s","1","v",0,1,0,1)])]),[EditDecision("d","montage","Tighten",2)])
  self.assertEqual(edit.timeline.ordered_video()[0].id,"a");self.assertEqual(SubtitleTrack([CaptionCue("Maya","Hi",2,3),CaptionCue("Maya","Go",0,1)]).ordered()[0].text,"Go")
if __name__=="__main__":unittest.main()
