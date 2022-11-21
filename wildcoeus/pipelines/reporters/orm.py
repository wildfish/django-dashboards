from typing import Optional

from django.utils import timezone

from wildcoeus.pipelines import BasePipelineReporter

from ..models import PipelineExecution, PipelineLog, TaskLog
from ..status import PipelineTaskStatus


class ORMReporter(BasePipelineReporter):
    def report(
        self,
        pipeline_id: Optional[str],
        pipeline_task: Optional[str],
        task_id: Optional[str],
        status: PipelineTaskStatus,
        message: str,
    ):
        if pipeline_id:
            PipelineLog.objects.create(
                pipeline_id=pipeline_id, status=status.value, message=message
            )

        else:
            TaskLog.objects.create(
                pipeline_task=pipeline_task,
                task_id=task_id,
                status=status.value,
                message=message,
            )
