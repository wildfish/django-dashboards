from typing import Any, Optional

from wildcoeus.pipelines import PipelineReporter

from ..models import PipelineLog, TaskLog


class ORMReporter(PipelineReporter):
    def report(
        self,
        pipeline_id: Optional[str],
        pipeline_task: Optional[str],
        task_id: Optional[str],
        status: str,
        message: str,
        serializable_pipeline_object: Optional[dict[str, Any]] = None,
        serializable_task_object: Optional[dict[str, Any]] = None,
    ):
        if pipeline_id:
            PipelineLog.objects.create(
                pipeline_id=pipeline_id, status=status, message=message
            )

        else:
            TaskLog.objects.create(
                pipeline_task=pipeline_task,
                task_id=task_id,
                status=status,
                message=message,
            )
