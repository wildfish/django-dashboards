from typing import Any, Optional

from wildcoeus.pipelines.status import PipelineTaskStatus


class PipelineReporter:
    def report(
        self,
        pipeline_id: Optional[str],
        pipeline_task: Optional[str],
        task_id: Optional[str],
        status: str,
        message: str,
        object_lookup: Optional[dict[str, Any]] = None,
    ):  # pragma: nocover
        pass

    def report_pipeline(
        self,
        pipeline_id: str,
        status: PipelineTaskStatus,
        message: str,
        object_lookup: Optional[dict[str, Any]] = None,
    ):
        self.report(pipeline_id, None, None, status, message, object_lookup)

    def report_task(
        self,
        pipeline_task: str,
        task_id: str,
        status: str,
        message: str,
        object_lookup: Optional[dict[str, Any]] = None,
    ):
        self.report(None, pipeline_task, task_id, status, message, object_lookup)
