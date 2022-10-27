from django.core.management.base import BaseCommand

from datorum.pipelines.runners.celery.tasks import run_pipeline


class Command(BaseCommand):
    help = "Simple command to start the demo pipeline in celery."

    def handle(self, *args, **options):
        run_pipeline.delay(
            pipeline_id="demo.basic.pipelines.BasicPipeline",
            input_data={"message": "Hi from Celery"},
        )
