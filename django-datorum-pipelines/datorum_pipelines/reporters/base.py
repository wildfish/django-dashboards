from enum import Enum
from typing import Optional


class PipelineTaskStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    CONFIG_ERROR = "CONFIG_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    CANCELLED = "CANCELLED"


class BasePipelineReporter:
    def report(
        self,
        pipeline_id: Optional[str],
        task_id: Optional[str],
        status: PipelineTaskStatus,
        message: str,
    ):  # pragma: nocover
        pass

    def report_pipeline(
        self, pipeline_id: str, status: PipelineTaskStatus, message: str
    ):
        self.report(pipeline_id, None, status, message)

    def report_task(self, task_id: str, status: PipelineTaskStatus, message: str):
        self.report(None, task_id, status, message)
