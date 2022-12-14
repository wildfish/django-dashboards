from typing import Any, Optional

from wildcoeus.pipelines import PipelineReporter
from wildcoeus.pipelines.log import logger


class LoggingReporter(PipelineReporter):
    def report(
        self,
        status: str,
        message: str,
        run_id: Optional[str] = None,
        pipeline_id: Optional[str] = None,
        task_id: Optional[str] = None,
        pipeline_task: Optional[str] = None,
        object_lookup: Optional[dict[str, Any]] = None,
    ):
        instance_msg = ""
        if object_lookup:
            instance_msg = f"for {object_lookup}"

        if pipeline_id:
            logger.info(
                f"Pipeline {pipeline_id} changed to state {status} {instance_msg}: {message}"
            )
        else:
            logger.info(
                f"Task {pipeline_task} ({task_id}) changed to state {status} {instance_msg}: {message}"
            )
