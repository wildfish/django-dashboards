from typing import Any, Optional, Union

from ..models import PipelineLog
from ..results.base import (
    BasePipelineExecution,
    BasePipelineResult,
    BaseTaskExecution,
    BaseTaskResult,
)
from ..status import PipelineTaskStatus
from . import PipelineReporter


class ORMReporter(PipelineReporter):
    def report(
        self,
        status: PipelineTaskStatus,
        message: str,
        context_object: Union[
            BasePipelineExecution, BasePipelineResult, BaseTaskExecution, BaseTaskResult
        ],
    ):
        PipelineLog.objects.create(
            context_type=type(context_object).__name__,
            context_id=context_object.id,
            pipeline_id=context_object.pipeline_id,
            run_id=context_object.run_id,
            status=status.value,
            message=message,
        )
