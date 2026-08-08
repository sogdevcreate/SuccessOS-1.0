from studio.screenwriting.screenplay import Screenplay
from studio.storyboard.camera_director import CameraDirector
from studio.storyboard.composition_analyzer import CompositionAnalyzer
from studio.storyboard.continuity_checker import ContinuityChecker
from studio.storyboard.lighting_director import LightingDirector
from studio.storyboard.storyboard import CinematicStoryboard


class StoryboardValidator:
    def __init__(self, camera_director: CameraDirector | None = None, lighting_director: LightingDirector | None = None, composition_analyzer: CompositionAnalyzer | None = None, continuity_checker: ContinuityChecker | None = None) -> None:
        self._camera_director = camera_director or CameraDirector()
        self._lighting_director = lighting_director or LightingDirector()
        self._composition_analyzer = composition_analyzer or CompositionAnalyzer()
        self._continuity_checker = continuity_checker or ContinuityChecker()

    def validate(self, storyboard: CinematicStoryboard, screenplay: Screenplay) -> list[str]:
        errors = self._continuity_checker.check(storyboard)
        screenplay_scenes = {scene.id: scene for scene in screenplay.scenes}
        for scene in storyboard.scenes:
            if scene.screenplay_scene_id not in screenplay_scenes:
                errors.append("Storyboard scene references an unknown screenplay scene")
            for shot in scene.sequence.shots:
                if shot.scene_id != scene.screenplay_scene_id:
                    errors.append(f"Shot '{shot.id}' scene traceability does not match its storyboard scene")
                if shot.scene_id not in screenplay_scenes:
                    errors.append(f"Shot '{shot.id}' references an unknown screenplay scene")
                if shot.source_screenplay_references and not set(shot.source_screenplay_references).issubset({shot.scene_id}):
                    errors.append(f"Shot '{shot.id}' has invalid screenplay references")
                errors.extend(self._camera_director.validate(shot.camera_plan))
                errors.extend(self._lighting_director.validate(shot.lighting_plan))
                errors.extend(self._composition_analyzer.validate(shot.composition))
        return errors
