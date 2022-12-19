from typing import Any, Optional


class PipelineReporter:
    def report(
        self,
        status: str,
        message: str,
        run_id: Optional[str] = None,
        pipeline_id: Optional[str] = None,
        task_id: Optional[str] = None,
        pipeline_task: Optional[str] = None,
        serializable_pipeline_object: Optional[dict[str, Any]] = None,
        serializable_task_object: Optional[dict[str, Any]] = None,
    ):  # pragma: nocover
        pass

    def report_pipeline(
        self,
        pipeline_id: str,
        status: str,
        message: str,
        run_id: Optional[str] = "",
        serializable_pipeline_object: Optional[dict[str, Any]] = None,
        serializable_task_object: Optional[dict[str, Any]] = None,
    ):
        self.report(
            pipeline_id=pipeline_id,
            run_id=run_id,
            status=status,
            message=message,
            serializable_pipeline_object=serializable_pipeline_object,
            serializable_task_object=serializable_task_object,
        )

    def report_task(
        self,
        pipeline_task: str,
        task_id: str,
        status: str,
        message: str,
        run_id: Optional[str] = "",
        serializable_pipeline_object: Optional[dict[str, Any]] = None,
        serializable_task_object: Optional[dict[str, Any]] = None,
    ):
        self.report(
            pipeline_task=pipeline_task,
            task_id=task_id,
            run_id=run_id,
            status=status,
            message=message,
            serializable_pipeline_object=serializable_pipeline_object,
            serializable_task_object=serializable_task_object,
        )
