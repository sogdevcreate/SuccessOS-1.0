from studio.research.fact import Fact


class FactExtractor:
    def normalize(self, facts: list[Fact]) -> list[Fact]:
        unique: dict[str, Fact] = {}
        for fact in facts:
            if fact.identifier in unique:
                raise ValueError(f"Duplicate fact identifier: {fact.identifier}")
            unique[fact.identifier] = fact
        return list(unique.values())
