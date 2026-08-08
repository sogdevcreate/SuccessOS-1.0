from dataclasses import dataclass,field
@dataclass
class PublicationManifest:
 project_version:str;final_master_reference:str;target_platform:str;provider:str="";external_publication_id:str="";metadata_reference:str="";provenance:dict[str,str]=field(default_factory=dict)
