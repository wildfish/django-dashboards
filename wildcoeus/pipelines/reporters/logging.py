from typing import Optional, Any

from wildcoeus.pipelines import PipelineReporter
from wildcoeus.pipelines.log import logger
from wildcoeus.pipelines.status import PipelineTaskStatus


class LoggingReporter(PipelineReporter):
    def report(
        self,
        pipeline_id: Optional[str],
        pipeline_task: Optional[str],
        task_id: Optional[str],
        status: PipelineTaskStatus,
        message: str,
        instance_lookup: Optional[dict[str, Any]],
    ):
        instance_msg = ""
        if instance_lookup:
            instance_msg = f"for {instance_lookup}"

        if pipeline_id:
            logger.info(
                f"Pipeline {pipeline_id} changed to state {status.value}: {message} {instance_msg}"
            )
        else:
            logger.info(
                f"Task {pipeline_task}:{task_id} changed to state {status.value}: {message} {instance_msg}"
            )
