import unittest
from studio.models import ProjectMetadata, StudioProject
from studio.post_production.color_grade import ColorGrade
from studio.post_production.color_profile import ColorProfile
from studio.post_production.edit_project import EditProject
from studio.post_production.export_profile import ExportProfile
from studio.post_production.render_profile import RenderProfile
from studio.post_production.render_request import RenderRequest
from studio.post_production.render_result import RenderResult, RenderResultStatus


class PostProductionSerializationTests(unittest.TestCase):
    def project(self) -> StudioProject:
        profile = RenderProfile("4K", 3840, 2160, "16:9", 24, "h264", "mp4", audio_codec="aac", sample_rate=48000)
        return StudioProject(metadata=ProjectMetadata("Film", "Creator"), edit_project=EditProject("Film"), color_grade=ColorGrade("grade", ColorProfile("cinema")), render_request=RenderRequest("project", "version", profile, ExportProfile("4K", "review", profile), "output/master.mp4", source_references=["edit", "audio"]), render_result=RenderResult(RenderResultStatus.APPROVED, "job-1", "sandbox://master.mp4"))

    def test_edit_project_round_trip(self) -> None:
        restored = StudioProject.from_dict(self.project().to_dict())
        self.assertEqual(restored.edit_project.title, "Film")

    def test_color_grade_round_trip(self) -> None:
        restored = StudioProject.from_dict(self.project().to_dict())
        self.assertEqual(restored.color_grade.id, "grade")

    def test_render_request_round_trip(self) -> None:
        restored = StudioProject.from_dict(self.project().to_dict())
        self.assertEqual(restored.render_request.render_profile.width, 3840)

    def test_render_result_round_trip(self) -> None:
        restored = StudioProject.from_dict(self.project().to_dict())
        self.assertEqual(restored.render_result.status, RenderResultStatus.APPROVED)

    def test_complete_post_production_round_trip(self) -> None:
        original = self.project()
        restored = StudioProject.from_dict(original.to_dict())
        self.assertEqual(restored.to_dict()["render_request"], original.to_dict()["render_request"])

    def test_legacy_project_without_post_production_fields(self) -> None:
        data = self.project().to_dict()
        for key in ("edit_project", "color_grade", "render_request", "render_result"):
            data.pop(key)
        restored = StudioProject.from_dict(data)
        self.assertIsNone(restored.edit_project)
        self.assertIsNone(restored.color_grade)
        self.assertIsNone(restored.render_request)
        self.assertIsNone(restored.render_result)
