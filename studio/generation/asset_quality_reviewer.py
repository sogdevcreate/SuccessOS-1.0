from studio.enums import PipelineStage
from studio.models.quality_report import QualityReport
from studio.models.quality_score import QualityScore
class AssetQualityReviewer:
    CRITERIA=("photorealism","identity_consistency","facial_consistency","body_consistency","wardrobe_continuity","environment_continuity","prop_continuity","composition_fidelity","lighting_fidelity","camera_fidelity","artifact_absence","anatomical_correctness","visual_coherence","directors_bible_compliance","production_profile_compliance")
    def review(self, asset, project):
        provenance=asset.provenance; score=10.0 if provenance.get("validated") == "true" else 0.0
        report=QualityReport(PipelineStage.ASSETS,[QualityScore(name, score) for name in self.CRITERIA],project.production_settings.quality_threshold); report.evaluate(); return report
