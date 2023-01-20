from typing import Any, Optional, Union

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
        status: PipelineTaskStatus,
        message: str,
        context_object: Union[
            BasePipelineExecution, BasePipelineResult, BaseTaskExecution, BaseTaskResult
        ],
    ):
        logger.info(message)
        if context_object:
            self._write_log_to_file(
                message + "\n",
                context_object.run_id,
            )

    @classmethod
    def _write_log_to_file(cls, content: str, run_id: Optional[str] = None):
        # need a run id to write file
        if not run_id:
            return

        fs = config.Config().WILDCOEUS_LOG_FILE_STORAGE
        path = get_log_path(run_id)
        d = now().strftime("%d/%b/%Y %H:%M:%S")
        content = f"[{d}]: {content}"

        if not fs.exists(path):
            fs.save(path, ContentFile(content))
        else:
            file = fs.open(path, "a+")
            file.write(content)
            fs.save(path, file)
            file.close()
