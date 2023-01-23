from typing import Union

from wildcoeus.pipelines.results.base import (
    BasePipelineExecution,
    BasePipelineResult,
    BaseTaskExecution,
    BaseTaskResult,
)
from wildcoeus.pipelines.status import PipelineTaskStatus


class PipelineReporter:
    def report(
        self,
        context_object: Union[
            BasePipelineExecution, BasePipelineResult, BaseTaskExecution, BaseTaskResult
        ],
        status: PipelineTaskStatus,
        message: str,
    ):  # pragma: nocover
        pass

    def report_pipeline_execution(
        self,
        pipeline_execution: BasePipelineExecution,
        status: PipelineTaskStatus,
        message: str,
    ):
        self.report(
            pipeline_execution,
            status,
            self._build_log_message(
                f"Pipeline {pipeline_execution.pipeline_id} changed to state {status.value}",
                status,
                message,
            ),
        )

    def report_pipeline_result(
        self,
        pipeline_result: BasePipelineResult,
        status: PipelineTaskStatus,
        message: str,
    ):
        self.report(
            pipeline_result,
            status,
            self._build_log_message(
                f"Pipeline result {pipeline_result.pipeline_id} changed to state {status.value}",
                status,
                message,
                pipeline_object=pipeline_result.serializable_pipeline_object,
            ),
        )

    def report_task_execution(
        self,
        task_execution: BaseTaskExecution,
        status: PipelineTaskStatus,
        message: str,
    ):
        self.report(
            task_execution,
            status,
            self._build_log_message(
                f"Task {task_execution.pipeline_task} ({task_execution.task_id}) changed to state {status.value}",
                status,
                message,
                pipeline_object=task_execution.serializable_pipeline_object,
            ),
        )

    def report_task_result(
        self,
        task_result: BaseTaskResult,
        status: PipelineTaskStatus,
        message: str,
    ):
        self.report(
            task_result,
            status,
            self._build_log_message(
                f"Task result {task_result.pipeline_task} ({task_result.task_id}) changed to state {status.value}",
                status,
                message,
                pipeline_object=task_result.serializable_pipeline_object,
                task_object=task_result.serializable_task_object,
            ),
        )

    def _build_log_message(
        self,
        root: str,
        status: PipelineTaskStatus,
        message: str,
        pipeline_object=None,
        task_object=None,
    ):
        message_parts = [message or status.value.capitalize()]

        if pipeline_object:
            message_parts.append(f"pipeline object: {pipeline_object}")

        if task_object:
            message_parts.append(f"task object: {task_object}")

        message = " | ".join(message_parts)

        return f"{root}: {message}"
