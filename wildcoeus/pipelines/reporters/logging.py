from typing import Union

from wildcoeus.pipelines.log import logger

from ..results.base import BasePipelineStorageObject
from ..status import PipelineTaskStatus
from . import PipelineReporter


class LoggingReporter(PipelineReporter):
    def report(
        self,
        context_object: BasePipelineStorageObject,
        status: PipelineTaskStatus,
        message: str,
    ):
        logger.info(message)
