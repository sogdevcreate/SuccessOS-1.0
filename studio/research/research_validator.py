from studio.research.research_report import ResearchReport


class ResearchValidator:
    def validate(self, report: ResearchReport) -> list[str]:
        errors: list[str] = []
        if not report.topic.strip():
            errors.append("Research topic is required")
        source_ids = {source.identifier for source in report.sources}
        if len(source_ids) != len(report.sources):
            errors.append("Research source identifiers must be unique")
        for fact in report.key_facts:
            if not fact.statement.strip():
                errors.append(f"Fact '{fact.identifier}' has no statement")
            if not fact.source_references:
                errors.append(f"Fact '{fact.identifier}' has no source references")
            unknown_sources = set(fact.source_references) - source_ids
            if unknown_sources:
                errors.append(f"Fact '{fact.identifier}' references unknown sources")
        for citation in report.citations:
            if citation.source_id not in source_ids:
                errors.append("Citation references an unknown source")
        return errors
