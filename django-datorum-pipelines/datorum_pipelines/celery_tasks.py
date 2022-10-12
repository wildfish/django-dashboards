from celery import shared_task
from datorum_pipelines.runners.eager import EagerRunner


@shared_task
def run_pipeline(pipeline_id, run_id, tasks, input_data, reporter):
    EagerRunner().start(
        pipeline_id,
        run_id,
        tasks,
        input_data,
        reporter,
    )
