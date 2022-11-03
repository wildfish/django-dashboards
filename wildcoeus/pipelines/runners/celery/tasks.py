import uuid

from celery import shared_task

from wildcoeus.pipelines import config
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.runners.eager import Runner


@shared_task
def run_pipeline(pipeline_id, input_data):
    """
    Start a specific pipeline's celery Runner.
    """
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    pipeline = pipeline_registry.get_pipeline_class(pipeline_id)
    tasks = pipeline().clean_tasks(reporter)

    Runner().start(
        pipeline_id=pipeline_id,
        run_id=str(uuid.uuid4()),
        tasks=tasks,
        input_data=input_data,
        reporter=reporter,
    )


@shared_task
def run_pipeline_report(pipeline_id, status, message):
    """
    Record a pipeline report update async.
    """
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    reporter.report_pipeline(pipeline_id=pipeline_id, status=status, message=message)


@shared_task
def run_task(task_id, pipeline_id, input_data):
    """
    Start a specific task via it's pipeline's runner.
    """
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    task = pipeline_registry.get_task_class(task_id)

    task.start(
        pipeline_id=pipeline_id,
        run_id=str(uuid.uuid4()),
        input_data=input_data,
        reporter=reporter,
    )


@shared_task
def run_task_report(task_id, pipeline_id, status, message):
    """
    Record a task report update async.
    """
    reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
    reporter.report_task(
        task_id=task_id, pipeline_id=pipeline_id, status=status, message=message
    )
