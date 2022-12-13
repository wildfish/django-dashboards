import uuid
import logging
from typing import Any, Dict, Optional

from celery import shared_task

from wildcoeus.pipelines import PipelineTaskStatus, config, task_registry
from wildcoeus.pipelines.registry import pipeline_registry
# from wildcoeus.pipelines.runners.celery.runner import Runner

logger = logging.getLogger(__name__)

@shared_task
def run_pipeline(pipeline_id: str, input_data: Dict[str, Any], run_id: Optional[str] = None):
    """
    Start a specific pipeline's celery Runner.
    """
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    runner = config.Config().WILDCOEUS_DEFAULT_PIPELINE_RUNNER
    pipeline_cls = pipeline_registry.get_pipeline_class(pipeline_id)
    if not run_id:
        run_id = str(uuid.uuid4())

    print("running in celery")
    print(run_id)
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
    print("run_pipeline_report")
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
    cleaned_config: Optional[dict[str, Any]],
):
    """
    Start a specific task via it's pipeline's runner.
    """
    logger.error(f"this is an error {task_id}")
    print("running celery run_task")
    print(task_id)
    print(run_id)
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    pipeline = pipeline_registry.get_pipeline_class(pipeline_id)
    tasks = pipeline().clean_tasks(reporter)
    task = list(filter(lambda x: x.task_id == task_id, tasks))[0]
    # print(f_task[0])
    # task = task_registry.get_task_class(task_id)(config=cleaned_config)
    print(task)
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
    logger.error(f"this is an error {status} =- {task_id}")
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    reporter.report_task(
        task_id=task_id,
        pipeline_id=pipeline_id,
        status=status,
        message=message,
        object_lookup=object_lookup,
    )
