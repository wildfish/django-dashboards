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
from wildcoeus.pipelines.status import FAILED_STATUES, PipelineTaskStatus
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


class PipelineExecutionQuerySet(QuerySet):
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
        return PipelineExecution.objects.annotate(
            task_count=Subquery(tasks_qs), duration=Subquery(duration_qs)
        )


class TaskResult(models.Model):
    pipeline_id = models.CharField(max_length=255)
    pipeline_task = models.CharField(max_length=255)
    task_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255)
    serializable_pipeline_object = models.JSONField(blank=True, null=True)
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
            task_id=self.task_id,
            run_id=self.run_id,
            config=self.config,
            reporter=reporter,
        )


class PipelineExecution(models.Model):
    pipeline_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255)
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

    objects = PipelineExecutionQuerySet.as_manager()

    def __str__(self):
        return f"{self.pipeline_id} started on {self.started}"

    def get_task_results(self):
        return TaskResult.objects.filter(run_id=self.run_id)

    @property
    def failed(self):
        return self.status in FAILED_STATUES

    class Meta:
        ordering = ["-started"]
        unique_together = ("run_id", "serializable_pipeline_object")


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
