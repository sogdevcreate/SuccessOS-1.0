import unittest
from studio.models import ProjectMetadata,StudioProject
from studio.post_production.render_result import RenderResult,RenderResultStatus
from studio.publishing.description_package import DescriptionPackage
from studio.publishing.disclosure_metadata import DisclosureMetadata
from studio.publishing.platform_profile import PlatformProfile
from studio.publishing.publish_request import PublishRequest
from studio.publishing.publishing_engine import PublishingEngine
from studio.publishing.publishing_provider_registry import PublishingProviderRegistry
from studio.publishing.publishing_provider_selector import PublishingProviderSelector
from studio.publishing.publishing_quality_reviewer import PublishingQualityReviewer
from studio.publishing.publishing_validator import PublishingValidator
from studio.publishing.publication_metadata import PublicationMetadata
from studio.publishing.rights_declaration import RightsDeclaration
from studio.publishing.tag_package import TagPackage
from studio.publishing.thumbnail_package import ThumbnailPackage
from studio.publishing.title_package import TitlePackage
class PublishingTests(unittest.TestCase):
 def request(self):
  rights=RightsDeclaration("owned","owned","licensed","licensed","licensed",commercial_use=True);return PublishRequest("p","v","sandbox://master","youtube",PlatformProfile("youtube",max_title_length=100),PublicationMetadata("Film","Desc","en"),TitlePackage(),DescriptionPackage("Desc"),ThumbnailPackage(selected_candidate="thumb"),TagPackage(),rights=rights,disclosures=DisclosureMetadata(),provenance={"render":"approved"})
 def test_rights_rejection_and_unavailable_provider(self):
  p=StudioProject(metadata=ProjectMetadata("Film","Creator"),render_result=RenderResult(RenderResultStatus.APPROVED,reference_uri="sandbox://master"),publish_request=self.request())
  result=PublishingEngine(PublishingProviderSelector(PublishingProviderRegistry()),PublishingValidator(),PublishingQualityReviewer())(type("C",(),{"project":p})());self.assertEqual(result.status.value,"failed");self.assertEqual(p.publish_result.status.value,"unavailable")
  self.assertFalse(RightsDeclaration().resolved)
if __name__=="__main__":unittest.main()
