from studio.models.quality_score import QualityScore
class VoiceQualityReviewer:
 CRITERIA=("realism","identity_consistency","emotional_performance","pronunciation","clarity","pacing","timing","lip_sync_compatibility","character_consistency","directors_bible_compliance")
 def scores(self,validated):return [QualityScore(x,10. if validated else 0.) for x in self.CRITERIA]
