from typing import Optional, Any

from wildcoeus.pipelines.status import PipelineTaskStatus


class PipelineReporter:
    def report(
        self,
        pipeline_id: Optional[str],
        pipeline_task: Optional[str],
        task_id: Optional[str],
        status: PipelineTaskStatus,
        message: str,
        instance_lookup: Optional[dict[str, Any]],
    ):  # pragma: nocover
        pass

    def report_pipeline(
        self,
        pipeline_id: str,
        status: PipelineTaskStatus,
        message: str,
        instance_lookup: Optional[dict[str, Any]],
    ):
        self.report(pipeline_id, None, None, status, message, instance_lookup)

    def report_task(
        self,
        pipeline_task: str,
        task_id: str,
        status: PipelineTaskStatus,
        message: str,
        instance_lookup: Optional[dict[str, Any]],
    ):
        self.report(None, pipeline_task, task_id, status, message, instance_lookup)
