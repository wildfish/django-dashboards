import uuid
from typing import Any, Dict, Optional

from celery import shared_task

from wildcoeus.pipelines import config
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.results.helpers import (
    get_pipeline_execution,
    get_pipeline_result,
    get_task_execution,
    get_task_result,
)
from wildcoeus.pipelines.status import PipelineTaskStatus


class TaskError(Exception):
    pass


@shared_task
def run_pipeline(
    pipeline_id: str, input_data: Dict[str, Any], run_id: Optional[str] = None
):
    """
    Start a specific pipeline's celery Runner.

    :param pipeline_id: The id of the registered pipeline class
    :param input_data: The input data to pass to the pipeline
    :param run_id: The id to record results against
    """
    from wildcoeus.pipelines.runners.celery.runner import Runner

    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    runner = Runner()
    pipeline_cls = pipeline_registry.get_by_id(pipeline_id)

    if not run_id:
        run_id = str(uuid.uuid4())

    pipeline_cls().start(
        run_id=run_id,
        input_data=input_data,
        runner=runner,
        reporter=reporter,
    )


@shared_task
def run_pipeline_execution_report(
    *args,
    run_id=None,
    status: str = "",
    message: Optional[str] = None,
    **kwargs,
):
    """
    Updates the status of a pipeline execution.

    :param run_id: The id of the running pipeline instance
    :param status: The new status of the pipeline execution
    :param message: The message to record against the status change
    """
    pipeline_execution = get_pipeline_execution(run_id)
    if not pipeline_execution:
        return

    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    pipeline_execution.report_status_change(
        reporter,
        PipelineTaskStatus[status],
        message=message,
    )


@shared_task
def run_pipeline_result_report(
    *args,
    pipeline_result_id=None,
    status: str = "",
    message: Optional[str] = None,
    propagate: bool = True,
    **kwargs,
):
    """
    Updates the status of a pipeline result.

    :param pipeline_result_id: The id of pipeline result to update
    :param status: The new status of the pipeline result
    :param message: The message to record against the status change
    :param propagate: If true the status will be passed to the pipeline execution too
    """
    pipeline_result = get_pipeline_result(pipeline_result_id)
    if not pipeline_result:
        return

    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    pipeline_result.report_status_change(
        reporter,
        PipelineTaskStatus[status],
        message=message,
        propagate=propagate,
    )


@shared_task
def run_task_execution_report(
    *args,
    task_execution_id=None,
    status: str = "",
    message: Optional[str] = None,
    propagate: bool = True,
    **kwargs,
):
    """
    Updates the status of a task execution.

    :param task_execution_id: The id of task execution to update
    :param status: The new status of the task execution
    :param message: The message to record against the status change
    :param propagate: If true the status will be passed to the pipeline result too
    """
    task_execution = get_task_execution(task_execution_id)
    if not task_execution:
        return

    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    task_execution.report_status_change(
        reporter,
        PipelineTaskStatus[status],
        message=message,
        propagate=propagate,
    )


@shared_task
def run_task_result_report(
    *args,
    task_result_id=None,
    status: str = "",
    message: Optional[str] = None,
    propagate: bool = True,
    **kwargs,
):
    """
    Updates the status of a task result.

    :param task_result_id: The id of task result to update
    :param status: The new status of the task result
    :param message: The message to record against the status change
    :param propagate: If true the status will be passed to the task execution too
    """
    task_result = get_task_result(task_result_id)
    if not task_result:
        return

    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    task_result.report_status_change(
        reporter,
        PipelineTaskStatus[status],
        message=message,
        propagate=propagate,
    )


@shared_task
def run_task(task_result_id: str):
    """
    Start a specific task via it's pipeline's runner.

    :param task_result_id: The id of the task result representing the
    task to run
    """
    task_result = get_task_result(task_result_id)
    if not task_result:
        return

    task = task_result.get_task()

    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER

    task.start(task_result, reporter)
