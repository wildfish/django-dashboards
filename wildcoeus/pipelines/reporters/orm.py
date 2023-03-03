from ..models import PipelineLog
from ..results.base import PipelineStorageObject
from ..status import PipelineTaskStatus
from . import PipelineReporter


class ORMReporter(PipelineReporter):
    """
    A reporter class that writes messages to the django ORM.
    """

    def report(
        self,
        context_object: PipelineStorageObject,
        status: PipelineTaskStatus,
        message: str,
    ):
        PipelineLog.objects.create(
            context_type=context_object.content_type_name,
            context_id=context_object.get_id(),
            pipeline_id=context_object.get_pipeline_id(),
            run_id=context_object.get_run_id(),
            status=status.value,
            message=message,
        )
