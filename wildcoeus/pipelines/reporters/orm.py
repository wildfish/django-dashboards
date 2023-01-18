from typing import Any, Optional, Union

from ..models import PipelineLog, TaskLog
from . import PipelineReporter
from ..results.base import BasePipelineExecution, BasePipelineResult, BaseTaskExecution, BaseTaskResult
from ..status import PipelineTaskStatus


class ORMReporter(PipelineReporter):
    def report(
        self,
        status: PipelineTaskStatus,
        message: str,
        context_object: Union[BasePipelineExecution, BasePipelineResult, BaseTaskExecution, BaseTaskResult] = None,
    ):
        if isinstance(context_object, (BasePipelineExecution, BasePipelineResult)):
            PipelineLog.objects.create(
                pipeline_id=context_object.pipeline_id, run_id=context_object.run_id, status=status, message=message
            )

        elif isinstance(context_object, (BaseTaskExecution, BaseTaskResult)):
            TaskLog.objects.create(
                pipeline_task=context_object.pipeline_task,
                task_id=context_object.task_id,
                run_id=context_object.run_id,
                status=status,
                message=message,
            )
