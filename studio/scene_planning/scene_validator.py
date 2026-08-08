from studio.scene_planning.asset_spec_validator import AssetSpecValidator
class SceneValidator:
    def __init__(self, asset_validator=None): self._asset_validator = asset_validator or AssetSpecValidator()
    def validate(self, scene_plans, asset_specs, project) -> list[str]:
        errors = []; screenplay_ids = {scene.id for scene in project.screenplay.scenes}; storyboard_ids = {scene.screenplay_scene_id for scene in project.cinematic_storyboard.scenes}
        asset_ids = {spec.id for spec in asset_specs}
        for plan in scene_plans:
            if plan.screenplay_scene_id not in screenplay_ids or plan.storyboard_scene_id not in storyboard_ids: errors.append(f"Scene plan '{plan.scene_id}' has invalid upstream references")
            if not set(plan.required_assets).issubset(asset_ids): errors.append(f"Scene plan '{plan.scene_id}' references unknown assets")
            if plan.generation_order and not set(plan.generation_order).issubset(set(plan.required_assets)): errors.append(f"Scene plan '{plan.scene_id}' has invalid generation order")
        for spec in asset_specs: errors.extend(self._asset_validator.validate(spec))
        return errors
