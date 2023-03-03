from wildcoeus.pipelines.log import logger

from ..results.base import PipelineStorageObject
from ..status import PipelineTaskStatus
from . import PipelineReporter


class LoggingReporter(PipelineReporter):
    """
    A reporter class that writes messages to the standard python logging mechanism.
    """

    def report(
        self,
        context_object: PipelineStorageObject,
        status: PipelineTaskStatus,
        message: str,
    ):
        logger.info(message)
