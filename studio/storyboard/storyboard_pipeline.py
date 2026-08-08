from studio.screenwriting.screenplay import Screenplay
from studio.storyboard.shot_planner import ShotPlanner
from studio.storyboard.storyboard import CinematicStoryboard
from studio.storyboard.storyboard_validator import StoryboardValidator


class StoryboardPipeline:
    """Normalizes and validates supplied visual planning; it does not render assets."""

    def __init__(self, shot_planner: ShotPlanner | None = None, validator: StoryboardValidator | None = None) -> None:
        self._shot_planner = shot_planner or ShotPlanner()
        self._validator = validator or StoryboardValidator()

    def analyze(self, storyboard: CinematicStoryboard, screenplay: Screenplay) -> CinematicStoryboard:
        for scene in storyboard.scenes:
            scene.sequence = self._shot_planner.order(scene.sequence)
        errors = self._validator.validate(storyboard, screenplay)
        if errors:
            raise ValueError("; ".join(errors))
        return storyboard
