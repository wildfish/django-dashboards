import uuid
from typing import Any, Dict, Optional

from celery import shared_task

from wildcoeus.pipelines.runners.celery.runner import Runner
from wildcoeus.pipelines import config
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
    runner = Runner()
    pipeline_cls = pipeline_registry.get_pipeline_class(pipeline_id)

    if not run_id:
        run_id = str(uuid.uuid4())

    pipeline_cls().start(
        run_id=run_id,
        input_data=input_data,
        runner=runner,
        reporter=reporter,
    )


@shared_task
def run_pipeline_report(
    pipeline_id: str,
    run_id: str,
    status: str,
    message: str,
    serializable_pipeline_object: Optional[dict[str, Any]],
):
    """
    Record a pipeline report update async.
    """
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    reporter.report_pipeline(
        pipeline_id=pipeline_id,
        run_id=run_id,
        status=status,
        message=message,
        serializable_pipeline_object=serializable_pipeline_object,
    )


@shared_task
def run_task(
    task_id: str,
    run_id: str,
    pipeline_id: str,
    input_data: Dict[str, Any],
    serializable_pipeline_object: Optional[dict[str, Any]],
    serializable_task_object: Optional[dict[str, Any]],
):
    """
    Start a specific task via it's pipeline's runner.
    """
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    pipeline = pipeline_registry.get_pipeline_class(pipeline_id)
    tasks = pipeline().clean_tasks(reporter, run_id=run_id)
    try:
        task = list(filter(lambda x: x.task_id == task_id, tasks))[0]
    except IndexError:
        raise TaskError(f"cannot find task in pipeline {pipeline_id} with id {task_id}")

    task.start(
        pipeline_id=pipeline_id,
        run_id=run_id,
        input_data=input_data,
        reporter=reporter,
        serializable_pipeline_object=serializable_pipeline_object,
        serializable_task_object=serializable_task_object,
    )


@shared_task
def run_task_report(
    task_id: str,
    pipeline_task: str,
    run_id: str,
    status: str,
    message: str,
    serializable_pipeline_object: Optional[dict[str, Any]],
    serializable_task_object: Optional[dict[str, Any]],
):
    """
    Record a task report update async.
    """
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    reporter.report_task(
        pipeline_task=pipeline_task,
        task_id=task_id,
        run_id=run_id,
        status=status,
        message=message,
        serializable_pipeline_object=serializable_pipeline_object,
        serializable_task_object=serializable_task_object,
    )
