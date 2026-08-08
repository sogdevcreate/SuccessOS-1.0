import unittest
from studio.enums import PipelineStage,StageStatus
from studio.models import ProjectMetadata,StudioProject
from studio.post_production.color_grade import ColorGrade
from studio.post_production.color_profile import ColorProfile
from studio.post_production.edit_project import EditProject
from studio.post_production.export_profile import ExportProfile
from studio.post_production.render_engine import RenderEngine
from studio.post_production.render_profile import RenderProfile
from studio.post_production.render_provider_registry import RenderProviderRegistry
from studio.post_production.render_provider_selector import RenderProviderSelector
from studio.post_production.render_request import RenderRequest
from studio.post_production.render_validator import RenderValidator
from studio.post_production.render_quality_reviewer import RenderQualityReviewer
class RenderingTests(unittest.TestCase):
 def test_render_profile_and_unavailable_state(self):
  profile=RenderProfile("4K",3840,2160,"16:9",24,"h264","mp4",audio_codec="aac",sample_rate=48000);request=RenderRequest("p","v",profile,ExportProfile("YouTube 4K","youtube",profile),"output/master.mp4",source_references=["edit","audio"])
  self.assertEqual(RenderRequest.from_dict(request.to_dict()).render_profile.width,3840)
  p=StudioProject(metadata=ProjectMetadata("Film","Creator"),edit_project=EditProject("Film"),color_grade=ColorGrade("c",ColorProfile("p")),render_request=request);p.stage_statuses[PipelineStage.COLOR_GRADING]=StageStatus.SUCCEEDED
  result=RenderEngine(RenderProviderSelector(RenderProviderRegistry()),RenderValidator(),RenderQualityReviewer())(type("C",(),{"project":p})());self.assertEqual(result.status,StageStatus.FAILED);self.assertEqual(p.render_result.status.value,"unavailable")
if __name__=="__main__":unittest.main()
