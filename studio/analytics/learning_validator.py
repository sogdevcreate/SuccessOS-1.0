from studio.analytics.learning_recommendation import RecommendationState
class LearningValidator:
    def validate_recommendation(self, recommendation, signals):
        errors=[]; known={signal.id for signal in signals}
        if not recommendation.supporting_signal_ids: errors.append("Recommendation requires supporting evidence")
        if not set(recommendation.supporting_signal_ids).issubset(known): errors.append("Recommendation references unknown evidence")
        if recommendation.causal_claim: errors.append("Unsupported causal claims are prohibited")
        if not recommendation.provenance: errors.append("Recommendation requires provenance")
        if recommendation.confidence < 0 or recommendation.confidence > 1: errors.append("Recommendation confidence must be between 0 and 1")
        return errors
    def can_create_policy(self, recommendation): return recommendation.state is RecommendationState.APPROVED and bool(recommendation.provenance)
