from studio.scene_planning.asset_specification import AssetSpecification
from studio.scene_planning.provider_capability import ProviderCapability
class AssetSpecValidator:
    def validate(self, specification: AssetSpecification) -> list[str]:
        errors = []
        if not specification.visual_description: errors.append(f"Asset '{specification.id}' lacks a visual description")
        if not specification.generation_instruction.modalities: errors.append(f"Asset '{specification.id}' lacks generation modalities")
        if not specification.acceptance_criteria: errors.append(f"Asset '{specification.id}' lacks acceptance criteria")
        return errors
    def validate_provider(self, specification: AssetSpecification, capability: ProviderCapability) -> list[str]:
        instruction = specification.generation_instruction; errors = []
        if not set(instruction.modalities).issubset(capability.supported_modalities): errors.append("Provider does not support requested modality")
        if instruction.character_reference_conditioning and not capability.character_reference: errors.append("Provider does not support character reference conditioning")
        if instruction.camera_motion_conditioning and not capability.camera_motion: errors.append("Provider does not support camera motion conditioning")
        if instruction.depth_input and not capability.depth: errors.append("Provider does not support depth conditioning")
        if instruction.mask_input and not capability.segmentation_masks: errors.append("Provider does not support segmentation masks")
        if instruction.aspect_ratio and capability.supported_aspect_ratios and instruction.aspect_ratio not in capability.supported_aspect_ratios: errors.append("Provider does not support requested aspect ratio")
        if capability.max_duration_seconds and instruction.duration_seconds > capability.max_duration_seconds: errors.append("Provider duration limit is exceeded")
        return errors
