from typing import Any, Optional

from wildcoeus.pipelines import PipelineReporter
from wildcoeus.pipelines.log import logger


class LoggingReporter(PipelineReporter):
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
    ):
        pipeline_object_msg = None
        if serializable_pipeline_object:
            pipeline_object_msg = f"pipeline object: {serializable_pipeline_object}"

        task_object_msg = None
        if serializable_task_object:
            task_object_msg = f"task object: {serializable_task_object}"

        messages = [message, pipeline_object_msg]

        if pipeline_id:
            message = " | ".join([m for m in messages if m])
            logger.info(f"Pipeline {pipeline_id} changed to state {status}: {message}")
        else:
            messages.append(task_object_msg)
            message = " | ".join([m for m in messages if m])
            logger.info(
                f"Task {pipeline_task} ({task_id}) changed to state {status}: {message}"
            )
