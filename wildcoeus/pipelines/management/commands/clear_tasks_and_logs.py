from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from wildcoeus.pipelines import config
from wildcoeus.pipelines.models import OrmPipelineExecution, PipelineLog
from wildcoeus.pipelines.results.helpers import cleanup_task_results


class Command(BaseCommand):
    help = "Delete PipelineExecution, TaskResult and PipelineLog based on a deletion cutoff."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, required=False)

    def handle(self, *args, **options):
        days = options["days"]

        if not days:
            days = config.Config().WILDCOEUS_CLEAR_LOG_DAYS

        today = now().today()
        deletion_date = today - timedelta(days=days)

        run_ids = cleanup_task_results(before=deletion_date)

        if run_ids:
            PipelineLog.objects.filter(run_id__in=run_ids).delete()
