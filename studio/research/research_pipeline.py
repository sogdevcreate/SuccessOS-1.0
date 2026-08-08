from studio.research.contradiction_detector import ContradictionDetector
from studio.research.entity_extractor import EntityExtractor
from studio.research.fact_extractor import FactExtractor
from studio.research.keyword_extractor import KeywordExtractor
from studio.research.research_report import ResearchReport
from studio.research.research_validator import ResearchValidator
from studio.research.source_ranker import SourceRanker
from studio.research.topic_expander import TopicExpander


class ResearchPipeline:
    """Performs deterministic analysis of supplied evidence; it does not acquire sources."""

    def __init__(self, topic_expander: TopicExpander | None = None, keyword_extractor: KeywordExtractor | None = None, entity_extractor: EntityExtractor | None = None, fact_extractor: FactExtractor | None = None, source_ranker: SourceRanker | None = None, contradiction_detector: ContradictionDetector | None = None, validator: ResearchValidator | None = None) -> None:
        self._topic_expander = topic_expander or TopicExpander()
        self._keyword_extractor = keyword_extractor or KeywordExtractor()
        self._entity_extractor = entity_extractor or EntityExtractor()
        self._fact_extractor = fact_extractor or FactExtractor()
        self._source_ranker = source_ranker or SourceRanker()
        self._contradiction_detector = contradiction_detector or ContradictionDetector()
        self._validator = validator or ResearchValidator()

    def analyze(self, report: ResearchReport) -> ResearchReport:
        report.research_questions = self._topic_expander.expand(report.research_questions)
        report.key_facts = self._fact_extractor.normalize(report.key_facts)
        report.entities = self._entity_extractor.normalize(report.entities)
        report.sources = self._source_ranker.rank(report.sources)
        report.timeline = report.ordered_timeline()
        report.contradictions = self._contradiction_detector.detect(report.key_facts)
        if not report.keywords:
            report.keywords = self._keyword_extractor.extract(" ".join([report.topic, report.executive_summary, *[fact.statement for fact in report.key_facts]]))
        errors = self._validator.validate(report)
        if errors:
            raise ValueError("; ".join(errors))
        return report
