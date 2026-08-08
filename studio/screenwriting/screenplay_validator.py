from studio.research.research_report import ResearchReport
from studio.screenwriting.screenplay import Screenplay


class ScreenplayValidator:
    def validate(self, screenplay: Screenplay, research_report: ResearchReport) -> list[str]:
        errors: list[str] = []
        facts = {fact.identifier: fact for fact in research_report.key_facts}
        fact_ids = set(facts)
        disputed_ids = {fact.identifier for fact in research_report.disputed_claims}
        cited_source_ids = {citation.source_id for citation in research_report.citations}
        scene_ids: set[str] = set()
        for scene in screenplay.scenes:
            if scene.id in scene_ids:
                errors.append(f"Duplicate scene id: {scene.id}")
            scene_ids.add(scene.id)
            unknown_references = set(scene.fact_references) - fact_ids
            if unknown_references:
                errors.append(f"Scene '{scene.id}' references unknown facts")
            uncited_references = [fact_id for fact_id in scene.fact_references if fact_id in facts and not set(facts[fact_id].source_references).intersection(cited_source_ids)]
            if uncited_references:
                errors.append(f"Scene '{scene.id}' references facts without report citations")
            unmarked_disputes = set(scene.fact_references).intersection(disputed_ids) - set(scene.disputed_fact_references)
            if unmarked_disputes:
                errors.append(f"Scene '{scene.id}' does not identify disputed fact references")
            unknown_disputes = set(scene.disputed_fact_references) - disputed_ids
            if unknown_disputes:
                errors.append(f"Scene '{scene.id}' identifies non-disputed facts as disputed")
            for beat in scene.beats:
                if set(beat.fact_references) - fact_ids:
                    errors.append(f"Beat {beat.sequence} in scene '{scene.id}' references unknown facts")
                if any(fact_id in facts and not set(facts[fact_id].source_references).intersection(cited_source_ids) for fact_id in beat.fact_references):
                    errors.append(f"Beat {beat.sequence} in scene '{scene.id}' references facts without report citations")
        return errors
