import logging
from typing import Optional

from datorum_pipelines import BasePipelineReporter

from ..status import PipelineTaskStatus


def get_logger():  # pragma: no cover
    return logging.getLogger(__name__)


class LoggingReporter(BasePipelineReporter):
    def report(
        self,
        pipeline_id: Optional[str],
        task_id: Optional[str],
        status: PipelineTaskStatus,
        message: str,
    ):
        if pipeline_id:
            get_logger().info(
                f"Pipeline {pipeline_id} changed to state {status.value}: {message}"
            )
        else:
            get_logger().info(
                f"Task {task_id} changed to state {status.value}: {message}"
            )
