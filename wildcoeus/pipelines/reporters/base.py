from typing import Any, Optional

from wildcoeus.pipelines.status import PipelineTaskStatus


class PipelineReporter:
    def report(
        self,
        run_id: str,
        status: str,
        message: str,
        pipeline_id: Optional[str] = None,
        task_id: Optional[str] = None,
        pipeline_task: Optional[str] = None,
        object_lookup: Optional[dict[str, Any]] = None,
    ):  # pragma: nocover
        pass

    def report_pipeline(
        self,
        pipeline_id: str,
        run_id: str,
        status: PipelineTaskStatus,
        message: str,
        object_lookup: Optional[dict[str, Any]] = None,
    ):
        self.report(
            pipeline_id=pipeline_id,
            run_id=run_id,
            status=status,
            message=message,
            object_lookup=object_lookup,
        )

    def report_task(
        self,
        pipeline_task: str,
        task_id: str,
        run_id: str,
        status: str,
        message: str,
        object_lookup: Optional[dict[str, Any]] = None,
    ):
        self.report(
            pipeline_task=pipeline_task,
            task_id=task_id,
            run_id=run_id,
            status=status,
            message=message,
            object_lookup=object_lookup,
        )
