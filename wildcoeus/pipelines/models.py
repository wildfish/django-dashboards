import uuid
from typing import Sequence

from django.db import models
from django.db.models import (
    Count,
    ExpressionWrapper,
    F,
    OuterRef,
    Subquery,
    Sum,
    fields,
)
from django.db.models.query import QuerySet
from django.utils.functional import cached_property

from django_extensions.db.models import TimeStampedModel

from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.results.base import (
    PipelineExecution,
    PipelineResult,
    TaskExecution,
    TaskResult,
)
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks import Task
from wildcoeus.pipelines.tasks.registry import task_registry
from wildcoeus.pipelines.utils import get_object


class PipelineLog(TimeStampedModel):
    """
    Model to store pipeline logs in the database
    """
    context_type = models.CharField(max_length=255, choices=[
        PipelineExecution.content_type_name,
        PipelineResult.content_type_name,
        TaskExecution.content_type_name,
        TaskResult.content_type_name,
    ])
    """
    The type of object to log a message against (one of PipelineExecution, PipelineResult, TaskExecution and TaskResult)
    """

    context_id = models.CharField(max_length=255)
    """The id of the object to log a message against"""

    pipeline_id = models.CharField(max_length=255)
    """Id of the pipeline being ran"""

    run_id = models.CharField(max_length=255, blank=True)
    """The run_id of the object"""

    status = models.CharField(max_length=255, choices=PipelineTaskStatus.choices())
    """The status of the object"""

    message = models.TextField(blank=True)
    """The message to record"""

    @property
    def log_message(self):
        return self.message

    def __str__(self):
        return self.log_message


class OrmPipelineExecutionQuerySet(QuerySet):
    """
    Custom query set for managing pipeline execution objects.
    """
    def with_extra_stats(self):
        """
        Attaches extra properties to the pipeline execution queryset so that
        each of the objects conform to the results storage interface.
        """
        results_qs = (
            OrmPipelineResult.objects.values_list("execution__id")
            .filter(execution_id=OuterRef("id"))
            .annotate(total=Count("id"))
            .values("total")
        )
        tasks_qs = (
            OrmTaskResult.objects.values_list(
                "execution__pipeline_result__execution_id"
            )
            .filter(execution__pipeline_result__execution_id=OuterRef("id"))
            .annotate(total=Count("id"))
            .values("total")
        )
        duration_qs = (
            OrmTaskResult.objects.values("execution__pipeline_result__execution_id")
            .filter(
                execution__pipeline_result__execution__id=OuterRef("id"),
                status=PipelineTaskStatus.DONE.value,
            )
            .annotate(duration=Sum(F("completed") - F("started")))
            .values("duration")
        )
        return self.annotate(
            pipeline_result_count=Subquery(results_qs),
            task_result_count=Subquery(tasks_qs),
            duration=Subquery(duration_qs),
        )


class OrmPipelineExecution(PipelineExecution, models.Model):
    """
    Model to store pipeline execution status in the django ORM
    """

    pipeline_id = models.CharField(max_length=255)
    """The id of the registered pipeline class"""

    run_id = models.CharField(max_length=255, default=uuid.uuid4, unique=True)
    """The id of the run to link the execution to"""

    status = models.CharField(
        max_length=255,
        choices=PipelineTaskStatus.choices(),
        default=PipelineTaskStatus.PENDING.value,
        db_index=True,
    )
    """The current status of the execution"""

    input_data = models.JSONField(blank=True, null=True)
    """The data passed into the pipeline when ran"""

    started = models.DateTimeField(blank=True, null=True, default=None, db_index=True)
    """The date and time when the run was started"""

    completed = models.DateTimeField(blank=True, null=True, default=None, db_index=True)
    """The date and time when the run finishes (whether successful or not)"""

    objects = OrmPipelineExecutionQuerySet.as_manager()

    def get_pipeline_results(self) -> Sequence["PipelineResult"]:
        """
        Returns all pipeline results associated with this execution
        from the database
        """
        return self.results.all()

    def get_pipeline(self) -> Pipeline:
        """
        Returns the registered pipeline class
        """
        return pipeline_registry.get_by_id(self.pipeline_id)

    def get_status(self):
        """
        Returns the current status of the pipeline
        """
        return PipelineTaskStatus[self.status]


class OrmPipelineResultQuerySet(QuerySet):
    def for_run_id(self, run_id):
        """
        Fetches all pipeline results for a given run id

        :param run_id: The run id to fetch all objects for.
        """
        return self.filter(execution__run_id=run_id)

    def with_extra_stats(self):
        """
        Attaches extra properties to the pipeline result queryset so that
        each of the objects conform to the results storage interface.
        """
        tasks_qs = (
            OrmTaskResult.objects.values_list("id")
            .filter(execution__pipeline_result__execution_id=OuterRef("id"))
            .annotate(total=Count("id"))
            .values("total")
        )
        duration_qs = (
            OrmTaskResult.objects.values("id")
            .filter(
                execution__pipeline_result__execution__id=OuterRef("id"),
                status=PipelineTaskStatus.DONE.value,
            )
            .annotate(duration=Sum(F("completed") - F("started")))
            .values("duration")
        )
        return self.annotate(
            task_result_count=Subquery(tasks_qs), duration=Subquery(duration_qs)
        )


class OrmPipelineResult(PipelineResult, models.Model):
    """
    The status of a given pipeline result
    """
    execution = models.ForeignKey(
        OrmPipelineExecution,
        related_name="results",
        on_delete=models.CASCADE,
        null=True,
    )
    """The pipeline execution relating to the current pipeline run"""

    serializable_pipeline_object = models.JSONField(blank=True, null=True)
    """The object related to this results instance"""

    status = models.CharField(
        max_length=255,
        choices=PipelineTaskStatus.choices(),
        default=PipelineTaskStatus.PENDING.value,
        db_index=True,
    )
    """The current status of this result"""

    runner = models.CharField(max_length=255, blank=True, null=True)
    """The python path to the runner the pipeline was started with"""

    reporter = models.CharField(max_length=255, blank=True, null=True)
    """The python path to the reporter the pipeline was started with"""

    started = models.DateTimeField(blank=True, null=True, default=None, db_index=True)
    """The time the pipeline was started"""

    completed = models.DateTimeField(blank=True, null=True, default=None, db_index=True)
    """The date and time when the run finishes (whether successful or not)"""

    objects = OrmPipelineResultQuerySet.as_manager()

    class Meta:
        ordering = ["-started"]

    def __str__(self):
        return f"{self.pipeline_id} started on {self.started}"

    def get_status(self) -> PipelineTaskStatus:
        """
        Returns the current status of the pipeline
        """
        return PipelineTaskStatus[self.status]

    @property
    def pipeline_id(self):
        """
        The id of the registered pipeline class
        """
        return self.execution.pipeline_id

    @property
    def input_data(self):
        """
        The data the pipeline was started with
        """
        return self.execution.input_data

    def get_pipeline(self) -> Pipeline:
        """
        Returns the registered pipeline class
        """
        return self.execution.get_pipeline()

    def get_pipeline_execution(self) -> PipelineExecution:
        """
        Returns the parent pipeline execution object
        """
        return self.execution

    def get_task_executions(self) -> Sequence["TaskExecution"]:
        """
        Returns all task execution objects for this pipeline instance
        """
        return self.task_executions.all()

    @property
    def run_id(self):
        """
        The id of the run for this pipeline
        """
        return self.execution.run_id

    @property
    def failed(self):
        """
        True if the result is in a failed state, otherwise false
        """
        return self.status in PipelineTaskStatus.failed_statuses()

    @cached_property
    def pipeline_object(self):
        """
        The deserialized pipeline object for this pipeline instance
        """
        return get_object(self.serializable_pipeline_object)


class TaskExecutionQuerySet(QuerySet):
    def for_run_id(self, run_id):
        """
        Returns a queryset containing all task executions for the given run id

        :param run_id: The id of the run to filter by
        """
        return self.filter(pipeline_result__execution__run_id=run_id)

    def not_completed(self):
        """
        Returns all uncompleted task executions
        """
        statues = [PipelineTaskStatus.PENDING.value, PipelineTaskStatus.RUNNING.value]
        return self.filter(status__in=statues)

    def with_duration(self):
        """
        Annotates the queryset with the time it took for all tasks to complete
        """
        duration = ExpressionWrapper(
            F("completed") - F("started"), output_field=fields.DurationField()
        )
        return self.annotate(duration=duration)


class OrmTaskExecution(TaskExecution, models.Model):
    pipeline_result = models.ForeignKey(
        OrmPipelineResult,
        related_name="task_executions",
        on_delete=models.CASCADE,
        null=True,
    )
    """The pipeline result this task is linked to"""

    task_id = models.CharField(max_length=255)
    """The id of the registered task class"""

    pipeline_task = models.CharField(max_length=255)
    """The name of the task property on the piepline"""

    config = models.JSONField()
    """The configuration used to instantiate the task"""

    status = models.CharField(
        max_length=255,
        choices=PipelineTaskStatus.choices(),
        default=PipelineTaskStatus.PENDING.value,
        db_index=True,
    )
    """The string representation of the task status"""

    started = models.DateTimeField(blank=True, null=True, default=None, db_index=True)
    """The time the pipeline was started"""

    completed = models.DateTimeField(blank=True, null=True, default=None, db_index=True)
    """The date and time when the run finishes (whether successful or not)"""

    objects = TaskExecutionQuerySet.as_manager()

    def get_status(self):
        """Returns the status of the task"""
        return PipelineTaskStatus[self.status]

    @property
    def input_data(self):
        """Returns the input data the pipeline was started with"""
        return self.pipeline_result.input_data

    @property
    def pipeline_id(self):
        """The id of the registered pipeline class"""
        return self.pipeline_result.pipeline_id

    @property
    def run_id(self):
        """The id of the current pipeline run"""
        return self.pipeline_result.run_id

    @property
    def serializable_pipeline_object(self):
        """The serialized version of the object associated with the related pipeline instance"""
        return self.pipeline_result.serializable_pipeline_object

    def get_task_results(self) -> Sequence["TaskResult"]:
        """Returns all the task results objects for this execution"""
        return self.results.all()

    def get_task(self) -> Task:
        """Returns the registered task class"""
        return task_registry.load_task_from_id(
            self.pipeline_task,
            self.task_id,
            self.config,
        )

    @cached_property
    def pipeline_object(self):
        """An instance of the registered pipeline class"""
        return get_object(self.serializable_pipeline_object)


class OrmTaskResultQuerySet(QuerySet):
    def for_run_id(self, run_id):
        """
        Returns a queryset containing all task results for the given run id

        :param run_id: The id of the run to filter by
        """
        return self.filter(execution__pipeline_result__execution__run_id=run_id)

    def not_completed(self):
        """
        Returns all uncompleted task executions
        """
        statues = [PipelineTaskStatus.PENDING.value, PipelineTaskStatus.RUNNING.value]
        return self.filter(status__in=statues)

    def with_duration(self):
        """
        Annotates the queryset with the time it took for all tasks to complete
        """
        duration = ExpressionWrapper(
            F("completed") - F("started"), output_field=fields.DurationField()
        )
        return self.annotate(duration=duration)


class OrmTaskResult(TaskResult, models.Model):
    execution = models.ForeignKey(
        OrmTaskExecution, related_name="results", on_delete=models.CASCADE, null=True
    )
    """The task execution object the result is linked to"""

    serializable_task_object = models.JSONField(blank=True, null=True)
    """The serialized version of the object associated with this task instance"""

    status = models.CharField(
        max_length=255,
        choices=PipelineTaskStatus.choices(),
        default=PipelineTaskStatus.PENDING.value,
        db_index=True,
    )
    """The string representation of the task status"""

    started = models.DateTimeField(blank=True, null=True, default=None, db_index=True)
    """The time the pipeline was started"""

    completed = models.DateTimeField(blank=True, null=True, default=None, db_index=True)
    """The date and time when the run finishes (whether successful or not)"""

    objects = OrmTaskResultQuerySet.as_manager()

    def __str__(self):
        return f"{self.task_id} ({self.run_id})"

    def get_status(self):
        """Returns the status of the task"""
        return PipelineTaskStatus[self.status]

    @property
    def run_id(self):
        """The id of the current pipeline run"""
        return self.execution.run_id

    @property
    def task_id(self):
        """The id of the registered task class"""
        return self.execution.task_id

    @property
    def pipeline_task(self):
        """The name of the task property on the piepline"""
        return self.execution.pipeline_task

    @property
    def serializable_pipeline_object(self):
        """The serialized version of the object associated with the related pipeline instance"""
        return self.execution.serializable_pipeline_object

    @property
    def pipeline_id(self):
        """The id of the registered pipeline class"""
        return self.execution.pipeline_id

    @property
    def duration(self):
        """The time taken for the task to finish"""
        if (
            self.status == PipelineTaskStatus.DONE.value
            and self.completed
            and self.started
        ):
            return (self.completed - self.started).seconds

        return None

    @property
    def config(self):
        """The configuration used to instantiate the task"""
        return self.execution.config

    @property
    def input_data(self):
        """Returns the input data the pipeline was started with"""
        return self.execution.input_data

    def get_task_execution(self) -> TaskExecution:
        """Returns the linked task execution"""
        return self.execution

    def get_task(self):
        """Returns an instance of the registered task"""
        return task_registry.load_task_from_id(
            pipeline_task=self.pipeline_task,
            task_id=self.task_id,
            config=self.config,
        )

    @cached_property
    def pipeline_object(self):
        """The deserialized version of the object linked to the pipeline instance"""
        return get_object(self.serializable_pipeline_object)

    @cached_property
    def task_object(self):
        """The deserialized version of the object linked to the task instance"""
        return get_object(self.serializable_task_object)
