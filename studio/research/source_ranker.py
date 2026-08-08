from studio.research.research_source import ResearchSource


class SourceRanker:
    def rank(self, sources: list[ResearchSource]) -> list[ResearchSource]:
        """Sorts evidence by equally weighted reliability and topic relevance."""
        return sorted(sources, key=lambda source: (source.reliability_score + source.relevance_score, source.reliability_score), reverse=True)
