import uuid
from typing import Any, Dict, Optional

from celery import shared_task

from wildcoeus.pipelines import config
from wildcoeus.pipelines.log import logger
from wildcoeus.pipelines.registry import pipeline_registry


class TaskError(Exception):
    pass


@shared_task
def run_pipeline(
    pipeline_id: str, input_data: Dict[str, Any], run_id: Optional[str] = None
):
    """
    Start a specific pipeline's celery Runner.
    """
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    runner = config.Config().WILDCOEUS_DEFAULT_PIPELINE_RUNNER
    pipeline_cls = pipeline_registry.get_pipeline_class(pipeline_id)
    if not run_id:
        run_id = str(uuid.uuid4())

    logger.debug(f"run_pipeline triggered with run_id {run_id}")

    pipeline_cls().start(
        run_id=run_id,
        input_data=input_data,
        runner=runner,
        reporter=reporter,
    )


@shared_task
def run_pipeline_report(
    pipeline_id: str,
    status: str,
    message: str,
    object_lookup: Optional[dict[str, Any]],
):
    """
    Record a pipeline report update async.
    """
    logger.debug(f"run_pipeline_report triggered for task {pipeline_id}")

    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    reporter.report_pipeline(
        pipeline_id=pipeline_id,
        status=status,
        message=message,
        object_lookup=object_lookup,
    )


@shared_task
def run_task(
    task_id: str,
    run_id: str,
    pipeline_id: str,
    input_data: Dict[str, Any],
    object_lookup: Optional[dict[str, Any]],
):
    """
    Start a specific task via it's pipeline's runner.
    """
    logger.debug(f"run_task triggered for task_id {task_id} and run_id {run_id}")

    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    pipeline = pipeline_registry.get_pipeline_class(pipeline_id)
    tasks = pipeline().clean_tasks(reporter)

    logger.debug(f"{tasks} found in pipeline {pipeline_id}")

    try:
        task = list(filter(lambda x: x.task_id == task_id, tasks))[0]
    except IndexError:
        raise TaskError(f"cannot find task in pipeline {pipeline_id} with id {task_id}")

    task.start(
        pipeline_id=pipeline_id,
        run_id=run_id,
        input_data=input_data,
        reporter=reporter,
        object_lookup=object_lookup,
    )


@shared_task
def run_task_report(
    task_id: str,
    pipeline_id: str,
    status: str,
    message: str,
    object_lookup: Optional[dict[str, Any]],
):
    """
    Record a task report update async.
    """
    logger.debug(f"run_task_report triggered for task {task_id}")

    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    reporter.report_task(
        task_id=task_id,
        pipeline_id=pipeline_id,
        status=status,
        message=message,
        object_lookup=object_lookup,
    )
