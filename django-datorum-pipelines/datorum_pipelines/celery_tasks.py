from celery import shared_task

from datorum_pipelines.pipelines.registry import pipeline_registry
from datorum_pipelines.reporters.logging import LoggingReporter
from datorum_pipelines.runners.eager import Runner


@shared_task
def run_pipeline(pipeline_id, run_id, input_data):
    reporter = LoggingReporter()
    pipeline = pipeline_registry.get_pipeline_class(pipeline_id)
    tasks = pipeline().clean_tasks(reporter)

    Runner().start(
        pipeline_id,
        run_id,
        tasks,
        input_data,
        reporter,
    )
