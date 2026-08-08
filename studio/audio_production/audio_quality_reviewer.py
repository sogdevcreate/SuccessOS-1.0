from studio.models.quality_score import QualityScore
class AudioQualityReviewer:
 CRITERIA=("dialogue_clarity","voice_consistency","mix_balance","sound_realism","ambience","foley_coverage","music_integration","synchronization","continuity","cinematic_impact","production_profile_compliance","directors_bible_compliance")
 def scores(self,validated):return [QualityScore(x,10. if validated else 0.) for x in self.CRITERIA]
