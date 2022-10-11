from django.db import models

from django_extensions.db.models import TimeStampedModel

from .status import PipelineTaskStatus


class PipelineLog(TimeStampedModel):
    pipeline_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, choices=PipelineTaskStatus.choices())
    message = models.TextField(blank=True)


class TaskLog(TimeStampedModel):
    task_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=255,
        choices=PipelineTaskStatus.choices(),
        default=PipelineTaskStatus.PENDING,
    )
    message = models.TextField(blank=True)


class TaskResult(models.Model):
    task_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=PipelineTaskStatus.choices())
    input_data = models.JSONField(blank=True, null=True)
    output_data = models.JSONField(blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True)
    completed = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("task_id", "run_id")

    def __str__(self):
        return f"{self.task_id} ({self.run_id})"


class PipelineExecution(models.Model):
    pipeline_id = models.TextField(unique=True)
    last_run = models.DateTimeField()

    def __str__(self):
        return f"{self.pipeline_id} started on {self.last_run}"
