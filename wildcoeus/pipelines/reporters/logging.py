from typing import Union

from wildcoeus.pipelines.log import logger

from ..results.base import (
    BasePipelineExecution,
    BasePipelineResult,
    BaseTaskExecution,
    BaseTaskResult,
)
from ..status import PipelineTaskStatus
from . import PipelineReporter


class LoggingReporter(PipelineReporter):
    def report(
        self,
        context_object: Union[
            BasePipelineExecution, BasePipelineResult, BaseTaskExecution, BaseTaskResult
        ],
        status: PipelineTaskStatus,
        message: str,
    ):
        logger.info(message)
