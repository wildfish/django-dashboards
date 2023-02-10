import logging
from typing import Callable, Union

from django.utils.module_loading import import_string

from wildcoeus.pipelines.results.base import (
    BasePipelineExecution,
    BasePipelineResult,
    BasePipelineStorageObject,
    BaseTaskExecution,
    BaseTaskResult,
)
from wildcoeus.pipelines.status import PipelineTaskStatus


class PipelineReporter:
    def report(
        self,
        context_object: BasePipelineStorageObject,
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
        self.report_context_object(pipeline_execution, status, message)

    def report_pipeline_result(
        self,
        pipeline_result: BasePipelineResult,
        status: PipelineTaskStatus,
        message: str,
    ):
        self.report_context_object(pipeline_result, status, message)

    def report_task_execution(
        self,
        task_execution: BaseTaskExecution,
        status: PipelineTaskStatus,
        message: str,
    ):
        self.report_context_object(task_execution, status, message)

    def report_task_result(
        self,
        task_result: BaseTaskResult,
        status: PipelineTaskStatus,
        message: str,
    ):
        self.report_context_object(task_result, status, message)

    def report_context_object(
        self,
        context_object: BasePipelineStorageObject,
        status: PipelineTaskStatus,
        message: str,
    ):
        message_builder: Callable[
            [BasePipelineStorageObject, PipelineTaskStatus, str], str
        ] = {
            BasePipelineExecution.content_type_name: self._build_pipeline_execution_message,
            BasePipelineResult.content_type_name: self._build_pipeline_result_message,
            BaseTaskExecution.content_type_name: self._build_task_execution_message,
            BaseTaskResult.content_type_name: self._build_task_result_message,
        }[
            context_object.content_type_name
        ]  # type: ignore

        self.report(
            context_object,
            status,
            message_builder(context_object, status, message),
        )

    def _build_pipeline_execution_message(
        self,
        pipeline_execution: BasePipelineExecution,
        status: PipelineTaskStatus,
        message: str,
    ):
        return self._build_log_message(
            f"Pipeline execution ({pipeline_execution.get_run_id()}) {pipeline_execution.get_pipeline_id()}",
            status,
            message,
        )

    def _build_pipeline_result_message(
        self,
        pipeline_result: BasePipelineResult,
        status: PipelineTaskStatus,
        message: str,
    ):
        return self._build_log_message(
            f"Pipeline result ({pipeline_result.get_id()}) {pipeline_result.get_pipeline_id()}",
            status,
            message,
            pipeline_object=pipeline_result.serializable_pipeline_object,
        )

    def _build_task_execution_message(
        self,
        task_execution: BaseTaskExecution,
        status: PipelineTaskStatus,
        message: str,
    ):
        return self._build_log_message(
            f"Task execution ({task_execution.get_id()}) {task_execution.get_pipeline_task()} ({task_execution.get_task_id()})",
            status,
            message,
            pipeline_object=task_execution.serializable_pipeline_object,
        )

    def _build_task_result_message(
        self, task_result: BaseTaskResult, status: PipelineTaskStatus, message: str
    ):
        return self._build_log_message(
            f"Task result ({task_result.get_id()}) {task_result.get_pipeline_task()} ({task_result.get_task_id()})",
            status,
            message,
            pipeline_object=task_result.get_serializable_pipeline_object(),
            task_object=task_result.get_serializable_task_object(),
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


class MultiPipelineReporter(PipelineReporter):
    def __init__(self, reporters):
        logging.info(reporters)
        self.reporters = [reporter_from_config(reporter) for reporter in reporters]

    def report(self, *args, **kwargs):
        for reporter in self.reporters:
            reporter.report(*args, **kwargs)


def reporter_from_config(reporter):
    if isinstance(reporter, str):
        return import_string(reporter)()

    module_path, params = reporter
    return import_string(module_path)(**params)
