from django.db import models

from django_extensions.db.models import TimeStampedModel

from datorum.pipelines.status import PipelineTaskStatus
from datorum.pipelines.tasks.registry import task_registry


class PipelineLog(TimeStampedModel):
    pipeline_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, choices=PipelineTaskStatus.choices())
    message = models.TextField(blank=True)


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


class TaskResult(models.Model):
    pipeline_id = models.CharField(max_length=255)
    pipeline_task = models.CharField(max_length=255)
    task_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=PipelineTaskStatus.choices())
    config = models.JSONField(blank=True, null=True)
    input_data = models.JSONField(blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True)
    completed = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("task_id", "run_id")

    def __str__(self):
        return f"{self.task_id} ({self.run_id})"

    @property
    def duration(self):
        if self.completed and self.started:
            return (self.completed - self.started).seconds

        return None

    def get_task_instance(self, reporter):
        return task_registry.load_task_from_id(
            pipeline_task=self.pipeline_task,
            task_id=self.task_id,
            config=self.config,
            reporter=reporter,
        )


class PipelineExecution(models.Model):
    pipeline_id = models.CharField(max_length=255, unique=True)
    last_run = models.DateTimeField()

    def __str__(self):
        return f"{self.pipeline_id} started on {self.last_run}"


class ValueStore(TimeStampedModel):
    """
    Used to pass lightweight data between tasks
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
