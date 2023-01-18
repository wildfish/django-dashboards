from typing import Union

from wildcoeus.pipelines.results.base import BasePipelineExecution, BaseTaskResult, BaseTaskExecution, \
    BasePipelineResult
from wildcoeus.pipelines.status import PipelineTaskStatus


class PipelineReporter:
    def report(
        self,
        status: PipelineTaskStatus,
        message: str,
        context_object: Union[BasePipelineExecution, BasePipelineResult, BaseTaskExecution, BaseTaskResult] = None,
    ):  # pragma: nocover
        pass

    def report_pipeline_execution(
        self,
        pipeline_execution: BasePipelineExecution,
        status: PipelineTaskStatus,
        message: str,
    ):
        self.report(
            status,
            f"Pipeline {pipeline_execution.pipeline_id} changed to state {status.value}: {message}",
            context_object=pipeline_execution,
        )

    def report_pipeline_result(
        self,
        pipeline_result: BasePipelineResult,
        status: PipelineTaskStatus,
        message: str,
    ):
        pipeline_object_msg = None
        if pipeline_result.serializable_pipeline_object:
            pipeline_object_msg = f"pipeline object: {pipeline_result.serializable_pipeline_object}"

        message_parts = [message, pipeline_object_msg]
        message = " | ".join([m for m in message_parts if m])

        self.report(
            status,
            f"Pipeline result {pipeline_result.pipeline_id} changed to state {status.value}: {message}",
            context_object=pipeline_result,
        )

    def report_task_execution(
        self,
        task_execution: BaseTaskExecution,
        status: PipelineTaskStatus,
        message: str,
    ):
        pipeline_object_msg = None
        if task_execution.serializable_pipeline_object:
            pipeline_object_msg = f"pipeline object: {task_execution.serializable_pipeline_object}"

        message_parts = [message, pipeline_object_msg]
        message = " | ".join([m for m in message_parts if m])

        self.report(
            status,
            f"Task {task_execution.pipeline_task} ({task_execution.task_id}) changed to state {status.value}: {message}",
            context_object=task_execution,
        )

    def report_task_result(
        self,
        task_result: BaseTaskResult,
        status: PipelineTaskStatus,
        message: str,
    ):
        pipeline_object_msg = None
        if task_result.serializable_pipeline_object:
            pipeline_object_msg = f"pipeline object: {task_result.serializable_pipeline_object}"

        task_object_msg = None
        if task_result.serializable_task_object:
            task_object_msg = f"task object: {task_result.serializable_task_object}"

        message_parts = [message, pipeline_object_msg, task_object_msg]
        message = " | ".join([m for m in message_parts if m])

        self.report(
            status,
            f"Task result {task_result.pipeline_task} ({task_result.task_id}) changed to state {status.value}: {message}",
            context_object=task_result,
        )
