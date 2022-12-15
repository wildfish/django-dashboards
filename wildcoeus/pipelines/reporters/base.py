from typing import Any, Optional


class PipelineReporter:
    def report(
        self,
        pipeline_id: Optional[str],
        pipeline_task: Optional[str],
        task_id: Optional[str],
        status: str,
        message: str,
        serializable_pipeline_object: Optional[dict[str, Any]] = None,
        serializable_task_object: Optional[dict[str, Any]] = None,
    ):  # pragma: nocover
        pass

    def report_pipeline(
        self,
        pipeline_id: str,
        status: str,
        message: str,
        serializable_pipeline_object: Optional[dict[str, Any]] = None,
        serializable_task_object: Optional[dict[str, Any]] = None,
    ):
        self.report(
            pipeline_id,
            None,
            None,
            status,
            message,
            serializable_pipeline_object,
            serializable_task_object,
        )

    def report_task(
        self,
        pipeline_task: str,
        task_id: str,
        status: str,
        message: str,
        serializable_pipeline_object: Optional[dict[str, Any]] = None,
        serializable_task_object: Optional[dict[str, Any]] = None,
    ):
        self.report(
            None,
            pipeline_task,
            task_id,
            status,
            message,
            serializable_pipeline_object,
            serializable_task_object,
        )
