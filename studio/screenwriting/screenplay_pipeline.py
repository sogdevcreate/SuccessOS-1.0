from studio.research.research_report import ResearchReport
from studio.screenwriting.beat_planner import BeatPlanner
from studio.screenwriting.continuity_checker import ContinuityChecker
from studio.screenwriting.dialogue_planner import DialoguePlanner
from studio.screenwriting.hook_generator import HookGenerator
from studio.screenwriting.narration_planner import NarrationPlanner
from studio.screenwriting.outline_builder import OutlineBuilder
from studio.screenwriting.pacing_analyzer import PacingAnalyzer
from studio.screenwriting.screenplay import Screenplay
from studio.screenwriting.screenplay_validator import ScreenplayValidator


class ScreenplayPipeline:
    """Deterministically validates supplied screenplay material; it does not generate it."""

    def __init__(self, hook_generator: HookGenerator | None = None, outline_builder: OutlineBuilder | None = None, beat_planner: BeatPlanner | None = None, dialogue_planner: DialoguePlanner | None = None, narration_planner: NarrationPlanner | None = None, pacing_analyzer: PacingAnalyzer | None = None, continuity_checker: ContinuityChecker | None = None, validator: ScreenplayValidator | None = None) -> None:
        self._hook_generator = hook_generator or HookGenerator()
        self._outline_builder = outline_builder or OutlineBuilder()
        self._beat_planner = beat_planner or BeatPlanner()
        self._dialogue_planner = dialogue_planner or DialoguePlanner()
        self._narration_planner = narration_planner or NarrationPlanner()
        self._pacing_analyzer = pacing_analyzer or PacingAnalyzer()
        self._continuity_checker = continuity_checker or ContinuityChecker()
        self._validator = validator or ScreenplayValidator()

    def analyze(self, screenplay: Screenplay, research_report: ResearchReport) -> Screenplay:
        screenplay.hook = self._hook_generator.normalize(screenplay.hook)
        screenplay.story_structure = self._outline_builder.normalize(screenplay.story_structure)
        for scene in screenplay.scenes:
            scene.beats = self._beat_planner.order(scene.beats)
            scene.dialogue = self._dialogue_planner.normalize(scene.dialogue)
            scene.narration = self._narration_planner.normalize(scene.narration)
        screenplay.tension_curve = self._pacing_analyzer.analyze(screenplay)
        errors = self._continuity_checker.check(screenplay) + self._validator.validate(screenplay, research_report)
        if errors:
            raise ValueError("; ".join(errors))
        return screenplay
