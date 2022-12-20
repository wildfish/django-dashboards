from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from wildcoeus.pipelines import config
from wildcoeus.pipelines.models import (
    PipelineExecution,
    PipelineLog,
    TaskLog,
    TaskResult,
)


class Command(BaseCommand):
    help = "Delete PipelineExecution, TaskResult, TaskLog and PipelineLog based on a deletion cutoff."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, required=False)

    def handle(self, *args, **options):
        days = options["days"]

        if not days:
            days = config.Config().WILDCOEUS_CLEAR_LOG_DAYS

        today = now().today()
        deletion_date = today - timedelta(days=days)
        PipelineExecution.objects.filter(started__lt=deletion_date).delete()
        TaskResult.objects.filter(started__lt=deletion_date).delete()
        TaskLog.objects.filter(created__lt=deletion_date).delete()
        PipelineLog.objects.filter(created__lt=deletion_date).delete()
