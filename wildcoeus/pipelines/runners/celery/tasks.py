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
    pipeline_execution_id=None,
    status: str = "",
    message: Optional[str] = None,
    **kwargs,
):
    """
    Record a pipeline report update async.
    """
    pipeline_execution = get_pipeline_execution(pipeline_execution_id)
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
    Record a pipeline report update async.
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
    Record a task report update async.
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
    Record a task report update async.
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
    """
    task_result = get_task_result(task_result_id)
    if not task_result:
        return

    task = task_result.get_task()

    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER

    task.start(task_result, reporter)
