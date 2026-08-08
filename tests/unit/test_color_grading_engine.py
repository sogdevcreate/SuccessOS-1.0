import unittest
from studio.enums import PipelineStage,StageStatus
from studio.models import DirectorsBible,ProductionProfile,ProjectMetadata,StudioProject
from studio.post_production.color_grade import ColorGrade
from studio.post_production.color_grading_engine import ColorGradingEngine
from studio.post_production.color_profile import ColorProfile
from studio.post_production.color_quality_reviewer import ColorQualityReviewer
from studio.post_production.edit_project import EditProject
from studio.post_production.exposure_adjustment import ExposureAdjustment
from studio.post_production.look_profile import LookProfile
from studio.post_production.shot_grade import ShotGrade
from studio.post_production.shot_match_plan import ShotMatchPlan
class ColorGradingTests(unittest.TestCase):
 def project(self):
  p=StudioProject(metadata=ProjectMetadata("Film","Creator"),production_profile=ProductionProfile(realism_level="photorealistic",visual_style="cinematic"),directors_bible=DirectorsBible(visual_rules=["natural skin"]),edit_project=EditProject("Film"));p.stage_statuses[PipelineStage.VIDEO_EDIT]=StageStatus.SUCCEEDED;p.color_grade=ColorGrade("grade",ColorProfile("cinema",look_profile=LookProfile("natural",["teal","orange"])),[ShotGrade("s1","scene",exposure=ExposureAdjustment(1),per_shot_overrides={"weather":"rain"})],[ShotMatchPlan("s1","s2",time_of_day="night",weather_state="rain")]);return p
 def test_serialization_adjustments_and_matching(self):
  grade=self.project().color_grade;restored=ColorGrade.from_dict(grade.to_dict());self.assertEqual(restored.shot_grades[0].exposure.stops,1);self.assertTrue(restored.shot_grades[0].saturation.skin_tone_protection);self.assertEqual(restored.shot_match_plans[0].weather_state,"rain")
 def test_quality_and_video_edit_gate(self):
  p=self.project();self.assertTrue(ColorQualityReviewer().review(p.color_grade,p).passed);self.assertEqual(ColorGradingEngine(ColorQualityReviewer()).grade(p).status,StageStatus.SUCCEEDED);p.stage_statuses[PipelineStage.VIDEO_EDIT]=StageStatus.PENDING;self.assertEqual(ColorGradingEngine(ColorQualityReviewer()).grade(p).status,StageStatus.FAILED)
if __name__=="__main__":unittest.main()
