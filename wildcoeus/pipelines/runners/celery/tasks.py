import logging
import uuid
from typing import Any, Dict, Optional

from celery import shared_task

from wildcoeus.pipelines import PipelineTaskStatus, config, task_registry
from wildcoeus.pipelines.registry import pipeline_registry


logger = logging.getLogger(__name__)


@shared_task
def run_pipeline(
    pipeline_id: str, input_data: Dict[str, Any], run_id: Optional[str] = None
):
    """
    Start a specific pipeline's celery Runner.
    """
    from wildcoeus.pipelines.runners.celery.runner import Runner

    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    pipeline_cls = pipeline_registry.get_pipeline_class(pipeline_id)

    if not run_id:
        run_id = str(uuid.uuid4())

    pipeline_cls().start(
        run_id=run_id,
        input_data=input_data,
        runner=Runner(),
        reporter=reporter,
    )


@shared_task
def run_pipeline_report(
    pipeline_id: str,
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
    tasks = pipeline().clean_tasks(reporter)
    task = list(filter(lambda x: x.task_id == task_id, tasks))[0]
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
    pipeline_id: str,
    status: str,
    message: str,
    serializable_pipeline_object: Optional[dict[str, Any]],
    serializable_task_object: Optional[dict[str, Any]],
):
    """
    Record a task report update async.
    """
    logger.error(f"this is an error {status} =- {task_id}")
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    reporter.report_task(
        task_id=task_id,
        pipeline_id=pipeline_id,
        status=status,
        message=message,
        serializable_pipeline_object=serializable_pipeline_object,
        serializable_task_object=serializable_task_object,
    )
