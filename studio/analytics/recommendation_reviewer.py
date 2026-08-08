from studio.analytics.learning_recommendation import RecommendationState
class RecommendationReviewer:
    def transition(self, recommendation, state):
        state=RecommendationState(state)
        allowed={RecommendationState.PROPOSED:{RecommendationState.UNDER_REVIEW,RecommendationState.REJECTED},RecommendationState.UNDER_REVIEW:{RecommendationState.APPROVED,RecommendationState.REJECTED},RecommendationState.APPROVED:{RecommendationState.SUPERSEDED,RecommendationState.DISABLED},RecommendationState.SUPERSEDED:set(),RecommendationState.REJECTED:set(),RecommendationState.DISABLED:set()}
        if state not in allowed[recommendation.state]: raise ValueError("Invalid recommendation review transition")
        recommendation.state=state
        return recommendation
