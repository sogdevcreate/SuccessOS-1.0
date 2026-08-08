from studio.analytics.analytics_report import AnalyticsReport
from studio.enums import PipelineStage
from studio.pipeline.stage_result import StageResult
class AnalyticsEngine:
    def __init__(self, selector): self._selector=selector
    def __call__(self, context):
        project=context.project
        if project.publish_result is None or project.publish_result.status.value!="completed": return StageResult.failed(PipelineStage.ANALYTICS,"Analytics requires completed publication")
        provider=self._selector.select()
        if provider is None:
            project.analytics_reports.append(AnalyticsReport("unavailable-"+project.identifier,project.identifier,project.publish_result.publication_reference,unavailable=True,errors=["No analytics provider is configured"]))
            return StageResult.failed(PipelineStage.ANALYTICS,"No analytics provider is configured")
        return StageResult.failed(PipelineStage.ANALYTICS,"No provider result is available; analytics remains pending")
