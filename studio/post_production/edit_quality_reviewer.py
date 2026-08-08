from studio.enums import PipelineStage
from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore
class EditQualityReviewer:
    CRITERIA=("narrative_clarity","pacing","continuity","cut_quality","transition_quality","dialogue_sync","music_sync","sound_sync","emotional_rhythm","cinematic_flow","screenplay_fidelity","directors_bible_compliance")
    def review(self,edit,project):
        valid=bool(edit.timeline.ordered_video() and edit.decisions);score=10. if valid else 0.;report=QualityReport(PipelineStage.VIDEO_EDIT,[QualityScore(x,score) for x in self.CRITERIA],project.production_settings.quality_threshold);report.evaluate();return report
