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

from django_extensions.db.models import TimeStampedModel

from wildcoeus.pipelines import config
from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.status import FAILED_STATUES, PipelineTaskStatus
from wildcoeus.pipelines.tasks import Task
from wildcoeus.pipelines.tasks.registry import task_registry


class PipelineLog(TimeStampedModel):
    pipeline_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, choices=PipelineTaskStatus.choices())
    message = models.TextField(blank=True)

    @property
    def log_message(self):
        return f"Pipeline {self.pipeline_id} changed to state {self.get_status_display()}: {self.message}"

    def __str__(self):
        return self.log_message


class TaskLog(TimeStampedModel):
    pipeline_task = models.CharField(max_length=255)
    task_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=255,
        choices=PipelineTaskStatus.choices(),
        default=PipelineTaskStatus.PENDING,
    )
    message = models.TextField(blank=True)

    @property
    def log_message(self):
        return f"Task {self.pipeline_task} ({self.task_id}) changed to state {self.get_status_display()}: {self.message}"

    def __str__(self):
        return self.log_message


class TaskResultQuerySet(QuerySet):
    def for_run_id(self, run_id):
        return self.filter(run_id=run_id)

    def not_completed(self):
        statues = [PipelineTaskStatus.PENDING.value, PipelineTaskStatus.RUNNING.value]
        return self.filter(status__in=statues)

    def with_duration(self):
        duration = ExpressionWrapper(
            F("completed") - F("started"), output_field=fields.DurationField()
        )
        return self.annotate(duration=duration)


class PipelineResultQuerySet(QuerySet):
    def with_task_count(self):
        tasks_qs = (
            TaskResult.objects.values_list("run_id")
            .filter(run_id=OuterRef("run_id"))
            .annotate(total=Count("task_id"))
            .values("total")
        )
        duration_qs = (
            TaskResult.objects.values("run_id")
            .filter(run_id=OuterRef("run_id"), status=PipelineTaskStatus.DONE.value)
            .annotate(duration=Sum(F("completed") - F("started")))
            .values("duration")
        )
        return PipelineResult.objects.annotate(
            task_count=Subquery(tasks_qs), duration=Subquery(duration_qs)
        )


class PipelineExecution(models.Model):
    started = models.DateTimeField(blank=True, null=True)
    pipeline_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255)

    def report_status_change(self, reporter: PipelineReporter, status: PipelineTaskStatus, message=""):
        if not PipelineTaskStatus[self.status].has_advanced(status):
            return

        self.status = status
        self.save()

        _msg = f"Pipeline execution {self.pipeline_id} changed to state"
        if message:
            _msg += f": {message}"

        reporter.report(
            status,
            _msg,
            run_id=self.run_id,
            pipeline_id=self.pipeline_id,
        )


class PipelineResult(models.Model):
    execution = models.ForeignKey(PipelineExecution, related_name="results", on_delete=models.CASCADE, null=True)
    serializable_pipeline_object = models.JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=255,
        choices=PipelineTaskStatus.choices(),
        default=PipelineTaskStatus.PENDING.value,
    )
    input_data = models.JSONField(blank=True, null=True)
    runner = models.CharField(max_length=255, blank=True, null=True)
    reporter = models.CharField(max_length=255, blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True)

    objects = PipelineResultQuerySet.as_manager()

    class Meta:
        ordering = ["-started"]

    def __str__(self):
        return f"{self.pipeline_id} started on {self.started}"

    def get_task_results(self):
        return TaskResult.objects.filter(run_id=self.run_id)

    @property
    def pipeline_id(self):
        return self.execution.pipeline_id

    @property
    def run_id(self):
        return self.execution.run_id

    @property
    def failed(self):
        return self.status in FAILED_STATUES

    def report_status_change(self, reporter: PipelineReporter, status: PipelineTaskStatus, propagate=True, message=""):
        if not PipelineTaskStatus[self.status].has_advanced(status):
            return

        if propagate:
            self.execution.report_status_change(reporter, status, message="")

        self.status = status
        self.save()

        _msg = f"Pipeline result {self.pipeline_id} changed to state"
        if message:
            _msg += f": {message}"

        if self.serializable_pipeline_object:
            _msg += f" | {self.serializable_pipeline_object}"

        reporter.report(
            status,
            _msg,
            run_id=self.run_id,
            pipeline_id=self.pipeline_id,
        )


class TaskExecution(models.Model):
    pipeline = models.ForeignKey(PipelineResult, related_name="tasks", on_delete=models.CASCADE, null=True)
    task_id = models.CharField(max_length=255)
    config = models.JSONField()

    def report_status_change(self, reporter: PipelineReporter | str, status: PipelineTaskStatus, propagate=True, message=""):
        if not PipelineTaskStatus[self.status].has_advanced(status):
            return

        if propagate:
            self.pipeline.report_status_change(reporter, status, message="")

        self.status = status
        self.save()

        _msg = f"Task execution {self.pipeline_id}:{self.task_id} changed to state"
        if message:
            _msg += f": {message}"

        if self.pipeline.serializable_pipeline_object:
            _msg += f" | {self.pipeline.serializable_pipeline_object}"

        reporter.report(
            status,
            _msg,
            run_id=self.run_id,
            pipeline_id=self.pipeline_id,
        )

    def get_task(self, reporter) -> Task:
        task_registry.load_task_from_id(
            self.pipeline.pipeline_id,
            self.task_id,
            self.pipeline.run_id,
            self.config,
            reporter,
        )


class TaskResult(models.Model):
    execution = models.ForeignKey(TaskExecution, related_name="results", on_delete=models.CASCADE, null=True)
    pipeline_task = models.CharField(max_length=255)
    serializable_task_object = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=PipelineTaskStatus.choices())
    config = models.JSONField(blank=True, null=True)
    input_data = models.JSONField(blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True)
    completed = models.DateTimeField(blank=True, null=True)

    objects = TaskResultQuerySet.as_manager()

    def __str__(self):
        return f"{self.task_id} ({self.run_id})"

    @property
    def run_id(self):
        return self.execution.pipeline.run_id

    @property
    def task_id(self):
        return self.execution.task_id

    @property
    def serializable_pipeline_object(self):
        return self.execution.pipeline.serializable_pipeline_object

    @property
    def pipeline_id(self):
        return self.execution.pipeline.pipeline_id

    @property
    def duration(self):
        if (
            self.status == PipelineTaskStatus.DONE.value
            and self.completed
            and self.started
        ):
            return (self.completed - self.started).seconds

        return None

    def get_task_instance(self):
        reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER

        return task_registry.load_task_from_id(
            pipeline_task=self.pipeline_task,
            task_id=self.execution.task_id,
            run_id=self.execution.pipeline_execution.run_id,
            config=self.config,
            reporter=reporter,
        )

    def report_status_change(self, reporter: PipelineReporter | str, status: PipelineTaskStatus, propagate=True, message=""):
        if not PipelineTaskStatus[self.status].has_advanced(status):
            return

        if propagate:
            self.execution.report_status_change(reporter, status, message="")

        self.status = status
        self.save()

        _msg = f"Task result {self.pipeline_id}:{self.task_id} changed to state"
        if message:
            _msg += f": {message}"

        if self.serializable_pipeline_object:
            _msg += f" | {self.serializable_pipeline_object}"

        if self.serializable_task_object:
            _msg += f" | {self.serializable_task_object}"

        reporter.report(
            str(status),
            _msg,
            run_id=self.run_id,
            pipeline_id=self.pipeline_id,
        )


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
