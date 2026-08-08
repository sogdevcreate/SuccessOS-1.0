from dataclasses import dataclass,field
from uuid import uuid4
from studio.publishing.chapter_package import ChapterPackage
from studio.publishing.description_package import DescriptionPackage
from studio.publishing.disclosure_metadata import DisclosureMetadata
from studio.publishing.platform_profile import PlatformProfile
from studio.publishing.publication_metadata import PublicationMetadata
from studio.publishing.rights_declaration import RightsDeclaration
from studio.publishing.scheduling_plan import SchedulingPlan
from studio.publishing.subtitle_package import SubtitlePackage
from studio.publishing.tag_package import TagPackage
from studio.publishing.thumbnail_package import ThumbnailPackage
from studio.publishing.title_package import TitlePackage
@dataclass
class PublishRequest:
 project_id:str;project_version:str;final_master_reference:str;target_platform:str;platform_profile:object;metadata:object;title_package:object;description_package:object;thumbnail_package:object;tags:object;chapters:list[object]=field(default_factory=list);subtitles:list[object]=field(default_factory=list);language:str="";audience_settings:dict[str,str]=field(default_factory=dict);visibility:str="";scheduling_plan:object|None=None;rights:object|None=None;disclosures:object|None=None;provenance:dict[str,str]=field(default_factory=dict);id:str=field(default_factory=lambda:str(uuid4()))
 def to_dict(self):
  return {"id":self.id,"project_id":self.project_id,"project_version":self.project_version,"final_master_reference":self.final_master_reference,"target_platform":self.target_platform,"platform_profile":self.platform_profile.to_dict(),"metadata":self.metadata.to_dict(),"title_package":self.title_package.to_dict(),"description_package":self.description_package.to_dict(),"thumbnail_package":self.thumbnail_package.to_dict(),"tags":self.tags.to_dict(),"chapters":[chapter.to_dict() for chapter in self.chapters],"subtitles":[subtitle.to_dict() for subtitle in self.subtitles],"language":self.language,"audience_settings":dict(self.audience_settings),"visibility":self.visibility,"scheduling_plan":self.scheduling_plan.to_dict() if self.scheduling_plan else None,"rights":self.rights.to_dict() if self.rights else None,"disclosures":self.disclosures.to_dict() if self.disclosures else None,"provenance":dict(self.provenance)}
 @classmethod
 def from_dict(cls,data):
  return cls(str(data["project_id"]),str(data["project_version"]),str(data["final_master_reference"]),str(data["target_platform"]),PlatformProfile.from_dict(data["platform_profile"]),PublicationMetadata.from_dict(data["metadata"]),TitlePackage.from_dict(data["title_package"]),DescriptionPackage.from_dict(data["description_package"]),ThumbnailPackage.from_dict(data["thumbnail_package"]),TagPackage.from_dict(data["tags"]),[ChapterPackage.from_dict(item) for item in data.get("chapters",[])],[SubtitlePackage.from_dict(item) for item in data.get("subtitles",[])],str(data.get("language","")),dict(data.get("audience_settings",{})),str(data.get("visibility","")),SchedulingPlan.from_dict(data["scheduling_plan"]) if data.get("scheduling_plan") else None,RightsDeclaration.from_dict(data["rights"]) if data.get("rights") else None,DisclosureMetadata.from_dict(data["disclosures"]) if data.get("disclosures") else None,dict(data.get("provenance",{})),str(data["id"]))
