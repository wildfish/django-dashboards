from typing import Optional

from wildcoeus.pipelines import BasePipelineReporter
from wildcoeus.pipelines.log import logger
from wildcoeus.pipelines.status import PipelineTaskStatus


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
