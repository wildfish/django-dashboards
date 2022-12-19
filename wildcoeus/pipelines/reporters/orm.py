from typing import Any, Optional

from wildcoeus.pipelines import PipelineReporter

from ..models import PipelineLog, TaskLog


class ORMReporter(PipelineReporter):
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
            PipelineLog.objects.create(
                pipeline_id=pipeline_id, run_id=run_id, status=status, message=message
            )

        else:
            messages.append(task_object_msg)
            message = " | ".join([m for m in messages if m])
            TaskLog.objects.create(
                pipeline_task=pipeline_task,
                task_id=task_id,
                run_id=run_id,
                status=status,
                message=message,
            )
