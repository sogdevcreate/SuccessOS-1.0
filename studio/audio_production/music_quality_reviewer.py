from studio.models.quality_score import QualityScore
class MusicQualityReviewer:
 CRITERIA=("emotional_fit","cinematic_quality","thematic_consistency","timing","scene_support","originality","continuity","directors_bible_compliance")
 def scores(self,validated):return [QualityScore(x,10. if validated else 0.) for x in self.CRITERIA]
