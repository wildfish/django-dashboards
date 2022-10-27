from typing import Optional

from datorum.pipelines import BasePipelineReporter
from datorum.pipelines.log import logger
from datorum.pipelines.status import PipelineTaskStatus


class LoggingReporter(BasePipelineReporter):
    def report(
        self,
        pipeline_id: Optional[str],
        pipeline_task: Optional[str],
        task_id: Optional[str],
        status: PipelineTaskStatus,
        message: str,
    ):
        if pipeline_id:
            logger.info(
                f"Pipeline {pipeline_id} changed to state {status.value}: {message}"
            )
        else:
            logger.info(
                f"Task {pipeline_task}:{task_id} changed to state {status.value}: {message}"
            )
