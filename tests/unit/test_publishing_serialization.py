import unittest

from studio.models import ProjectMetadata, StudioProject
from studio.post_production.export_profile import ExportProfile
from studio.post_production.render_profile import RenderProfile
from studio.post_production.render_request import RenderRequest
from studio.post_production.render_result import RenderResult, RenderResultStatus
from studio.publishing.chapter_package import ChapterPackage
from studio.publishing.description_package import DescriptionPackage
from studio.publishing.disclosure_metadata import DisclosureMetadata
from studio.publishing.platform_profile import PlatformProfile
from studio.publishing.publication_metadata import PublicationMetadata
from studio.publishing.publish_request import PublishRequest
from studio.publishing.publish_result import PublishResult, PublishResultStatus
from studio.publishing.rights_declaration import RightsDeclaration
from studio.publishing.scheduling_plan import SchedulingPlan
from studio.publishing.subtitle_package import SubtitlePackage
from studio.publishing.tag_package import TagPackage
from studio.publishing.thumbnail_package import ThumbnailPackage
from studio.publishing.title_package import TitleCandidate, TitlePackage


class PublishingSerializationTests(unittest.TestCase):
    def publish_request(self) -> PublishRequest:
        return PublishRequest(
            "project-1", "version-1", "sandbox://final/master.mp4", "youtube",
            PlatformProfile("youtube", 100, 5000, {"mp4"}, {"4K"}, {"16:9"}, 3600.0, True, True, "16:9", True, {"public"}, ["title"], ["synthetic_media"]),
            PublicationMetadata("A Film", "Description", "en", tags=["film"], credits=["Creator"]),
            TitlePackage([TitleCandidate("A Film", "viewers", "hook", ["film"], 9.0, True)]),
            DescriptionPackage("Description", "Short", ["Creator"], ["Source"], ["Chapter"], {"site": "example"}, ["synthetic"]),
            ThumbnailPackage("asset://thumb", ["asset://alt"], "16:9", "3840x2160", ["bottom"], ["Title"], "lead", ["character-1"], "Brand", "asset://thumb", {"source": "spec"}),
            TagPackage(["film"], ["cinematic"]),
            [ChapterPackage("Opening", 0.0, 30.0, ["scene-1"])],
            [SubtitlePackage("en", "asset://captions", "timeline-1", {"cc": "true"}, False, True, {"source": "edit"})],
            "en", {"made_for_kids": "false"}, "public",
            SchedulingPlan(False, "UTC", "2030-01-01T00:00:00Z", "", True, "future"),
            RightsDeclaration("owned", "owned", "licensed", "licensed", "licensed", "cleared", ["credit"], True),
            DisclosureMetadata(True, False, False, False, False, False, {"notice": "generated"}),
            {"render": "render-1"}, "publish-1",
        )

    def test_publish_request_round_trip_preserves_nested_models(self) -> None:
        restored = PublishRequest.from_dict(self.publish_request().to_dict())
        self.assertIsInstance(restored.platform_profile, PlatformProfile)
        self.assertEqual(restored.platform_profile.supported_formats, {"mp4"})
        self.assertIsInstance(restored.title_package.candidates[0], TitleCandidate)
        self.assertTrue(restored.title_package.candidates[0].selected)
        self.assertEqual(restored.chapters[0].scene_references, ["scene-1"])
        self.assertTrue(restored.subtitles[0].default)
        self.assertTrue(restored.rights.resolved)

    def test_publish_result_round_trip_preserves_enum(self) -> None:
        result = PublishResult(PublishResultStatus.COMPLETED, "publication-1", "https://example.test/video", "")
        restored = PublishResult.from_dict(result.to_dict())
        self.assertEqual(restored, result)
        self.assertIsInstance(restored.status, PublishResultStatus)

    def test_studio_project_round_trip_preserves_publishing_state(self) -> None:
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"), publish_request=self.publish_request(), publish_result=PublishResult(PublishResultStatus.FAILED, error="network"))
        restored = StudioProject.from_dict(project.to_dict())
        self.assertEqual(restored.publish_request.id, "publish-1")
        self.assertEqual(restored.publish_result.status, PublishResultStatus.FAILED)
        self.assertEqual(restored.publish_request.thumbnail_package.selected_candidate, "asset://thumb")

    def test_complete_render_and_publishing_round_trip(self) -> None:
        profile = RenderProfile("4K", 3840, 2160, "16:9", 24, "h264", "mp4", audio_codec="aac", sample_rate=48000)
        render_request = RenderRequest("project-1", "version-1", profile, ExportProfile("YouTube 4K", "youtube", profile), "sandbox://final/master.mp4", {"language": "en"}, ["edit", "audio"], ["color"], "9.0", "render-1")
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"), render_request=render_request, render_result=RenderResult(RenderResultStatus.APPROVED, "job-1", "sandbox://final/master.mp4"), publish_request=self.publish_request(), publish_result=PublishResult(PublishResultStatus.COMPLETED, "publication-1", "reference"))
        restored = StudioProject.from_dict(project.to_dict())
        self.assertEqual(restored.render_request.id, "render-1")
        self.assertEqual(restored.render_result.status, RenderResultStatus.APPROVED)
        self.assertEqual(restored.publish_request.scheduling_plan.timezone, "UTC")
        self.assertEqual(restored.publish_result.external_id, "publication-1")

    def test_legacy_project_without_publishing_fields_deserializes_to_none(self) -> None:
        project = StudioProject(metadata=ProjectMetadata("Film", "Creator"))
        legacy = project.to_dict()
        legacy.pop("publish_request", None)
        legacy.pop("publish_result", None)
        restored = StudioProject.from_dict(legacy)
        self.assertIsNone(restored.publish_request)
        self.assertIsNone(restored.publish_result)


if __name__ == "__main__":
    unittest.main()
