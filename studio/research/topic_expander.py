class TopicExpander:
    """Normalizes caller-supplied research questions without inventing claims."""

    def expand(self, questions: list[str]) -> list[str]:
        seen: set[str] = set()
        return [question.strip() for question in questions if question.strip() and not (question.casefold() in seen or seen.add(question.casefold()))]
