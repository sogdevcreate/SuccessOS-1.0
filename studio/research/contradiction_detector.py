from studio.research.fact import Fact, VerificationStatus


class ContradictionDetector:
    def detect(self, facts: list[Fact]) -> list[tuple[str, str]]:
        pairs: list[tuple[str, str]] = []
        for index, first in enumerate(facts):
            for second in facts[index + 1:]:
                if self._normalized(first.statement) == self._normalized(second.statement) and (first.disputed != second.disputed or first.verification_status is not second.verification_status):
                    pairs.append((first.identifier, second.identifier))
                    first.disputed = True
                    second.disputed = True
                    if second.identifier not in first.contradiction_references:
                        first.contradiction_references.append(second.identifier)
                    if first.identifier not in second.contradiction_references:
                        second.contradiction_references.append(first.identifier)
        return pairs

    @staticmethod
    def _normalized(statement: str) -> str:
        return " ".join(statement.casefold().split())
