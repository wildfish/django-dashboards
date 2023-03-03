from typing import Callable

from wildcoeus.config import object_from_config
from wildcoeus.pipelines.results.base import (
    PipelineExecution,
    PipelineResult,
    PipelineStorageObject,
    TaskExecution,
    TaskResult,
)
from wildcoeus.pipelines.status import PipelineTaskStatus


class PipelineReporter:
    """
    The base pipeline reporting object to reporting status messages about
    pipelines. This should be extended providing a :code:`report` method
    to implement a new reporting mechanism.
    """

    def report(
        self,
        context_object: PipelineStorageObject,
        status: PipelineTaskStatus,
        message: str,
    ):  # pragma: nocover
        """
        Writes the report to the report storage mechanism for a particular
        results storage object.

        :param context_object: The results storage object to write a report for
        :param status: The status of the context object being reported
        :param message: The message to record against the context object
        """
        raise NotImplementedError()

    def report_pipeline_execution(
        self,
        pipeline_execution: PipelineExecution,
        status: PipelineTaskStatus,
        message: str,
    ):
        """
        Writes the report to the report storage mechanism for a given
        :code:`PipelineExecution` object.

        :param pipeline_execution: The pipeline execution storage object to write
            a report for
        :param status: The status of the pipeline execution being reported
        :param message: The message to record against the context object
        """
        self.report_context_object(pipeline_execution, status, message)

    def report_pipeline_result(
        self,
        pipeline_result: PipelineResult,
        status: PipelineTaskStatus,
        message: str,
    ):
        """
        Writes the report to the report storage mechanism for a given
        :code:`PipelineResult` object.

        :param pipeline_result: The pipeline result storage object to write
            a report for
        :param status: The status of the pipeline result being reported
        :param message: The message to record against the context object
        """
        self.report_context_object(pipeline_result, status, message)

    def report_task_execution(
        self,
        task_execution: TaskExecution,
        status: PipelineTaskStatus,
        message: str,
    ):
        """
        Writes the report to the report storage mechanism for a given
        :code:`TaskExecution` object.

        :param task_execution: The task execution storage object to write
            a report for
        :param status: The status of the task execution being reported
        :param message: The message to record against the context object
        """
        self.report_context_object(task_execution, status, message)

    def report_task_result(
        self,
        task_result: TaskResult,
        status: PipelineTaskStatus,
        message: str,
    ):
        """
        Writes the report to the report storage mechanism for a given
        :code:`TaskResult` object.

        :param task_result: The task result storage object to write
            a report for
        :param status: The status of the task result being reported
        :param message: The message to record against the context object
        """
        self.report_context_object(task_result, status, message)

    def report_context_object(
        self,
        context_object: PipelineStorageObject,
        status: PipelineTaskStatus,
        message: str,
    ):
        """
        Writes the report to the report storage mechanism for a particular
        results storage object.

        The log message will be built based on the context object provided before
        being passed onto :code:`report`

        :param context_object: The results storage object to write a report for
        :param status: The status of the context object being reported
        :param message: The message to record against the context object
        """
        message_builder: Callable[
            [PipelineStorageObject, PipelineTaskStatus, str], str
        ] = {
            PipelineExecution.content_type_name: self._build_pipeline_execution_message,
            PipelineResult.content_type_name: self._build_pipeline_result_message,
            TaskExecution.content_type_name: self._build_task_execution_message,
            TaskResult.content_type_name: self._build_task_result_message,
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
        pipeline_execution: PipelineExecution,
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
        pipeline_result: PipelineResult,
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
        task_execution: TaskExecution,
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
        self, task_result: TaskResult, status: PipelineTaskStatus, message: str
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
    """
    A reporter class that allows reporting to multiple other reporter classes.
    """

    def __init__(self, reporters):
        """
        :params reporters: A list of reporters to include. Each element in the list is
            either a python path to the reporter class to use or a 2-tuple where the
            first element is the the python path to the reporter class and the second
            element is a dictionary of keyword arguments to pass to the reporter class
            on instantiation.
        """
        self.reporters = [object_from_config(reporter) for reporter in reporters]

    def report(self, *args, **kwargs):
        for reporter in self.reporters:
            reporter.report(*args, **kwargs)
