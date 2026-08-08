from dataclasses import dataclass, field

from studio.research.citation import Citation
from studio.research.entity import Entity, EntityType
from studio.research.fact import Fact, VerificationStatus
from studio.research.research_source import ResearchSource
from studio.research.timeline_event import TimelineEvent


@dataclass
class ResearchReport:
    topic: str
    research_questions: list[str] = field(default_factory=list)
    executive_summary: str = ""
    key_facts: list[Fact] = field(default_factory=list)
    unresolved_questions: list[str] = field(default_factory=list)
    timeline: list[TimelineEvent] = field(default_factory=list)
    entities: list[Entity] = field(default_factory=list)
    terminology: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    sources: list[ResearchSource] = field(default_factory=list)
    citations: list[Citation] = field(default_factory=list)
    contradictions: list[tuple[str, str]] = field(default_factory=list)
    visual_opportunities: list[str] = field(default_factory=list)
    suggested_scenes: list[str] = field(default_factory=list)
    suggested_archive_reference_needs: list[str] = field(default_factory=list)
    script_angles: list[str] = field(default_factory=list)
    hook_ideas: list[str] = field(default_factory=list)
    thumbnail_ideas: list[str] = field(default_factory=list)
    risk_notes: list[str] = field(default_factory=list)
    copyright_source_use_notes: list[str] = field(default_factory=list)

    @property
    def verified_facts(self) -> list[Fact]:
        return [fact for fact in self.key_facts if fact.verification_status is VerificationStatus.VERIFIED and not fact.disputed]

    @property
    def disputed_claims(self) -> list[Fact]:
        return [fact for fact in self.key_facts if fact.disputed or fact.verification_status is VerificationStatus.DISPUTED]

    @property
    def people(self) -> list[Entity]:
        return self._entities_of_type(EntityType.PERSON)

    @property
    def organizations(self) -> list[Entity]:
        return self._entities_of_type(EntityType.ORGANIZATION)

    @property
    def locations(self) -> list[Entity]:
        return self._entities_of_type(EntityType.LOCATION)

    @property
    def dates(self) -> list[Entity]:
        return self._entities_of_type(EntityType.DATE)

    @property
    def confidence_scores(self) -> dict[str, float]:
        return {fact.identifier: fact.confidence for fact in self.key_facts}

    def ordered_timeline(self) -> list[TimelineEvent]:
        return sorted(self.timeline, key=lambda event: event.event_date)

    def to_dict(self) -> dict[str, object]:
        return {"topic": self.topic, "research_questions": list(self.research_questions), "executive_summary": self.executive_summary, "key_facts": [fact.to_dict() for fact in self.key_facts], "unresolved_questions": list(self.unresolved_questions), "timeline": [event.to_dict() for event in self.timeline], "entities": [entity.to_dict() for entity in self.entities], "terminology": list(self.terminology), "keywords": list(self.keywords), "themes": list(self.themes), "sources": [source.to_dict() for source in self.sources], "citations": [citation.to_dict() for citation in self.citations], "contradictions": [list(pair) for pair in self.contradictions], "visual_opportunities": list(self.visual_opportunities), "suggested_scenes": list(self.suggested_scenes), "suggested_archive_reference_needs": list(self.suggested_archive_reference_needs), "script_angles": list(self.script_angles), "hook_ideas": list(self.hook_ideas), "thumbnail_ideas": list(self.thumbnail_ideas), "risk_notes": list(self.risk_notes), "copyright_source_use_notes": list(self.copyright_source_use_notes)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ResearchReport":
        return cls(topic=str(data["topic"]), research_questions=list(data.get("research_questions", [])), executive_summary=str(data.get("executive_summary", "")), key_facts=[Fact.from_dict(item) for item in data.get("key_facts", [])], unresolved_questions=list(data.get("unresolved_questions", [])), timeline=[TimelineEvent.from_dict(item) for item in data.get("timeline", [])], entities=[Entity.from_dict(item) for item in data.get("entities", [])], terminology=list(data.get("terminology", [])), keywords=list(data.get("keywords", [])), themes=list(data.get("themes", [])), sources=[ResearchSource.from_dict(item) for item in data.get("sources", [])], citations=[Citation.from_dict(item) for item in data.get("citations", [])], contradictions=[tuple(pair) for pair in data.get("contradictions", [])], visual_opportunities=list(data.get("visual_opportunities", [])), suggested_scenes=list(data.get("suggested_scenes", [])), suggested_archive_reference_needs=list(data.get("suggested_archive_reference_needs", [])), script_angles=list(data.get("script_angles", [])), hook_ideas=list(data.get("hook_ideas", [])), thumbnail_ideas=list(data.get("thumbnail_ideas", [])), risk_notes=list(data.get("risk_notes", [])), copyright_source_use_notes=list(data.get("copyright_source_use_notes", [])))

    def _entities_of_type(self, entity_type: EntityType) -> list[Entity]:
        return [entity for entity in self.entities if entity.entity_type is entity_type]
