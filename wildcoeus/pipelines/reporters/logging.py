from typing import Optional, Union

from django.core.files.base import ContentFile
from django.utils.timezone import now

from wildcoeus.pipelines import config
from wildcoeus.pipelines.log import logger
from wildcoeus.pipelines.storage import get_log_path

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
