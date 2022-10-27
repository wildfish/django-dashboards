from typing import Optional

from datorum.pipelines.status import PipelineTaskStatus


class BasePipelineReporter:
    def report(
        self,
        pipeline_id: Optional[str],
        pipeline_task: Optional[str],
        task_id: Optional[str],
        status: PipelineTaskStatus,
        message: str,
    ):  # pragma: nocover
        pass

    def report_pipeline(
        self, pipeline_id: str, status: PipelineTaskStatus, message: str
    ):
        self.report(pipeline_id, None, None, status, message)

    def report_task(
        self, pipeline_task: str, task_id: str, status: PipelineTaskStatus, message: str
    ):
        self.report(None, pipeline_task, task_id, status, message)
