import uuid
from typing import Any, Dict, Optional

from celery import shared_task

from wildcoeus.pipelines import PipelineTaskStatus, config, task_registry
from wildcoeus.pipelines.registry import pipeline_registry


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

    pipeline_cls().start(
        run_id=run_id,
        input_data=input_data,
        runner=runner,
        reporter=reporter,
    )


@shared_task
def run_pipeline_report(
    pipeline_id: str,
    status: PipelineTaskStatus,
    message: str,
    object_lookup: Optional[dict[str, Any]],
):
    """
    Record a pipeline report update async.
    """
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
    pipeline_id: str,
    input_data: Dict[str, Any],
    object_lookup: Optional[dict[str, Any]],
):
    """
    Start a specific task via it's pipeline's runner.
    """
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    task = task_registry.get_task_class(task_id)

    task.start(
        pipeline_id=pipeline_id,
        run_id=str(uuid.uuid4()),
        input_data=input_data,
        reporter=reporter,
        object_lookup=object_lookup,
    )


@shared_task
def run_task_report(
    task_id: str,
    pipeline_id: str,
    status: PipelineTaskStatus,
    message: str,
    object_lookup: Optional[dict[str, Any]],
):
    """
    Record a task report update async.
    """
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    reporter.report_task(
        task_id=task_id,
        pipeline_id=pipeline_id,
        status=status,
        message=message,
        object_lookup=object_lookup,
    )
