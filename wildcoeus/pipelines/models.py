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
from django.utils.timezone import now

from django_extensions.db.models import TimeStampedModel

from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import (
    BasePipelineExecution,
    BasePipelineResult,
    BaseTaskExecution,
    BaseTaskResult,
)
from wildcoeus.pipelines.status import FAILED_STATUES, PipelineTaskStatus
from wildcoeus.pipelines.tasks import Task
from wildcoeus.pipelines.tasks.registry import task_registry
from wildcoeus.pipelines.utils import get_object


class PipelineLog(TimeStampedModel):
    context_type = models.CharField(max_length=255)
    context_id = models.CharField(max_length=255)
    pipeline_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, choices=PipelineTaskStatus.choices())
    message = models.TextField(blank=True)

    @property
    def log_message(self):
        # return f"Pipeline {self.pipeline_id} changed to state {self.get_status_display()}: {self.message}"
        return self.message

    def __str__(self):
        return self.log_message


class TaskExecutionQuerySet(QuerySet):
    def for_run_id(self, run_id):
        return self.filter(pipeline_result__execution__run_id=run_id)

    def not_completed(self):
        statues = [PipelineTaskStatus.PENDING.value, PipelineTaskStatus.RUNNING.value]
        return self.filter(status__in=statues)

    def with_duration(self):
        duration = ExpressionWrapper(
            F("completed") - F("started"), output_field=fields.DurationField()
        )
        return self.annotate(duration=duration)


class TaskResultQuerySet(QuerySet):
    def for_run_id(self, run_id):
        return self.filter(execution__pipeline_result__execution__run_id=run_id)

    def not_completed(self):
        statues = [PipelineTaskStatus.PENDING.value, PipelineTaskStatus.RUNNING.value]
        return self.filter(status__in=statues)

    def with_duration(self):
        duration = ExpressionWrapper(
            F("completed") - F("started"), output_field=fields.DurationField()
        )
        return self.annotate(duration=duration)


class PipelineExecutionQuerySet(QuerySet):
    def with_extra_stats(self):
        results_qs = (
            PipelineResult.objects.values_list("execution__id")
            .filter(execution_id=OuterRef("id"))
            .annotate(total=Count("id"))
            .values("total")
        )
        tasks_qs = (
            TaskResult.objects.values_list("execution__pipeline_result__execution_id")
            .filter(execution__pipeline_result__execution_id=OuterRef("id"))
            .annotate(total=Count("id"))
            .values("total")
        )
        duration_qs = (
            TaskResult.objects.values("execution__pipeline_result__execution_id")
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


class PipelineExecution(BasePipelineExecution, models.Model):
    pipeline_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255,
        choices=PipelineTaskStatus.choices(),
        default=PipelineTaskStatus.PENDING.value,
    )
    input_data = models.JSONField(blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True, default=None)
    completed = models.DateTimeField(blank=True, null=True, default=None)

    objects = PipelineExecutionQuerySet.as_manager()

    def get_pipeline_results(self) -> Sequence["BasePipelineResult"]:
        return self.results.all()

    def get_pipeline(self) -> Pipeline:
        return pipeline_registry.get_by_id(self.pipeline_id)

    def get_status(self):
        return PipelineTaskStatus[self.status]

    def report_status_change(
        self, reporter: PipelineReporter, status: PipelineTaskStatus, message=""
    ):
        if not PipelineTaskStatus[self.status].has_advanced(status):
            return

        if status == PipelineTaskStatus.RUNNING:
            self.started = now()

        if status in PipelineTaskStatus.final_statuses():
            self.completed = now()

        self.status = status.value
        self.save()
        reporter.report_pipeline_execution(
            self,
            status,
            f"Changed state to {status.value}{'' if not message else ' - ' + message}",
        )


class PipelineResultQuerySet(QuerySet):
    def for_run_id(self, run_id):
        return self.filter(execution__run_id=run_id)

    def with_extra_stats(self):
        tasks_qs = (
            TaskResult.objects.values_list("id")
            .filter(execution__pipeline_result__execution_id=OuterRef("id"))
            .annotate(total=Count("id"))
            .values("total")
        )
        duration_qs = (
            TaskResult.objects.values("id")
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


class PipelineResult(BasePipelineResult, models.Model):
    execution = models.ForeignKey(
        PipelineExecution, related_name="results", on_delete=models.CASCADE, null=True
    )
    serializable_pipeline_object = models.JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=255,
        choices=PipelineTaskStatus.choices(),
        default=PipelineTaskStatus.PENDING.value,
    )
    runner = models.CharField(max_length=255, blank=True, null=True)
    reporter = models.CharField(max_length=255, blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True, default=None)
    completed = models.DateTimeField(blank=True, null=True, default=None)

    objects = PipelineResultQuerySet.as_manager()

    class Meta:
        ordering = ["-started"]

    def __str__(self):
        return f"{self.pipeline_id} started on {self.started}"

    def get_task_results(self):
        return TaskResult.objects.filter(run_id=self.run_id)

    def get_status(self):
        return PipelineTaskStatus[self.status]

    @property
    def pipeline_id(self):
        return self.execution.pipeline_id

    @property
    def input_data(self):
        return self.execution.input_data

    def get_pipeline(self) -> Pipeline:
        return self.execution.get_pipeline()

    def get_pipeline_execution(self) -> BasePipelineExecution:
        return self.execution

    def get_task_executions(self) -> Sequence["BaseTaskExecution"]:
        return self.task_executions.all()

    @property
    def run_id(self):
        return self.execution.run_id

    @property
    def failed(self):
        return self.status in FAILED_STATUES

    def report_status_change(
        self,
        reporter: PipelineReporter,
        status: PipelineTaskStatus,
        propagate=True,
        message="",
    ):
        if not PipelineTaskStatus[self.status].has_advanced(status):
            return

        if propagate:
            self.execution.report_status_change(reporter, status, message=message)

        if status == PipelineTaskStatus.RUNNING:
            self.started = now()

        if status in PipelineTaskStatus.final_statuses():
            self.completed = now()

        self.status = status.value
        self.save()
        reporter.report_pipeline_result(
            self,
            status,
            f"Changed state to {status.value}{'' if not message else ' - ' + message}",
        )

    @cached_property
    def pipeline_object(self):
        return get_object(self.serializable_pipeline_object)


class TaskExecution(BaseTaskExecution, models.Model):
    pipeline_result = models.ForeignKey(
        PipelineResult,
        related_name="task_executions",
        on_delete=models.CASCADE,
        null=True,
    )
    task_id = models.CharField(max_length=255)
    pipeline_task = models.CharField(max_length=255)
    config = models.JSONField()
    status = models.CharField(
        max_length=255,
        choices=PipelineTaskStatus.choices(),
        default=PipelineTaskStatus.PENDING.value,
    )
    started = models.DateTimeField(blank=True, null=True, default=None)
    completed = models.DateTimeField(blank=True, null=True, default=None)

    objects = TaskExecutionQuerySet.as_manager()

    def get_status(self):
        return PipelineTaskStatus[self.status]

    @property
    def input_data(self):
        return self.pipeline_result.input_data

    @property
    def pipeline_id(self):
        return self.pipeline_result.pipeline_id

    @property
    def run_id(self):
        return self.pipeline_result.run_id

    @property
    def serializable_pipeline_object(self):
        return self.pipeline_result.serializable_pipeline_object

    def get_task_results(self) -> Sequence["BaseTaskResult"]:
        return self.results.all()

    def report_status_change(
        self,
        reporter: PipelineReporter,
        status: PipelineTaskStatus,
        propagate=True,
        message="",
    ):
        if not PipelineTaskStatus[self.status].has_advanced(status):
            return

        if propagate:
            self.pipeline_result.report_status_change(reporter, status, message=message)

        if status == PipelineTaskStatus.RUNNING:
            self.started = now()

        if status in PipelineTaskStatus.final_statuses():
            self.completed = now()

        self.status = status.value
        self.save()
        reporter.report_task_execution(
            self,
            status,
            f"Changed state to {status.value}{'' if not message else ' - ' + message}",
        )

    def get_task(self) -> Task:
        return task_registry.load_task_from_id(
            self.pipeline_task,
            self.task_id,
            self.config,
        )

    @cached_property
    def pipeline_object(self):
        return get_object(self.serializable_pipeline_object)


class TaskResult(BaseTaskResult, models.Model):
    execution = models.ForeignKey(
        TaskExecution, related_name="results", on_delete=models.CASCADE, null=True
    )
    serializable_task_object = models.JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=255,
        choices=PipelineTaskStatus.choices(),
        default=PipelineTaskStatus.PENDING.value,
    )
    started = models.DateTimeField(blank=True, null=True, default=None)
    completed = models.DateTimeField(blank=True, null=True, default=None)

    objects = TaskResultQuerySet.as_manager()

    def __str__(self):
        return f"{self.task_id} ({self.run_id})"

    def get_status(self):
        return PipelineTaskStatus[self.status]

    @property
    def run_id(self):
        return self.execution.run_id

    @property
    def task_id(self):
        return self.execution.task_id

    @property
    def pipeline_task(self):
        return self.execution.pipeline_task

    @property
    def serializable_pipeline_object(self):
        return self.execution.serializable_pipeline_object

    @property
    def pipeline_id(self):
        return self.execution.pipeline_id

    @property
    def duration(self):
        if (
            self.status == PipelineTaskStatus.DONE.value
            and self.completed
            and self.started
        ):
            return (self.completed - self.started).seconds

        return None

    @property
    def config(self):
        return self.execution.config

    @property
    def input_data(self):
        return self.execution.input_data

    def get_task_execution(self) -> BaseTaskExecution:
        return self.execution

    def get_task_instance(self):
        return task_registry.load_task_from_id(
            pipeline_task=self.pipeline_task,
            task_id=self.task_id,
            config=self.config,
        )

    def report_status_change(
        self,
        reporter: PipelineReporter,
        status: PipelineTaskStatus,
        propagate=True,
        message="",
    ):
        if not PipelineTaskStatus[self.status].has_advanced(status):
            return

        if propagate:
            self.execution.report_status_change(reporter, status, message=message)

        if status == PipelineTaskStatus.RUNNING:
            self.started = now()

        if status in PipelineTaskStatus.final_statuses():
            self.completed = now()

        self.status = status.value
        self.save()
        reporter.report_task_result(
            self,
            status,
            f"Changed state to {status.value}{'' if not message else ' - ' + message}",
        )

    @cached_property
    def pipeline_object(self):
        return get_object(self.serializable_pipeline_object)

    @cached_property
    def task_object(self):
        return get_object(self.serializable_task_object)


class ValueStore(TimeStampedModel):
    """
    Used to store lightweight data between tasks
    """

    pipeline_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    value = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = ("pipeline_id", "run_id", "key")

    @classmethod
    def store(cls, pipeline_id, run_id, key, value):
        ValueStore.objects.update_or_create(
            pipeline_id=pipeline_id, run_id=run_id, key=key, defaults={"value": value}
        )

    @classmethod
    def get(cls, pipeline_id, run_id, key):
        try:
            data = ValueStore.objects.get(
                pipeline_id=pipeline_id, run_id=run_id, key=key
            )
        except ValueStore.DoesNotExist:
            return None

        return data.value
