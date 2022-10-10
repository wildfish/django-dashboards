from django.db import models

from django_extensions.db.models import TimeStampedModel

from .status import PipelineTaskStatus


class PipelineLog(TimeStampedModel):
    pipeline_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=PipelineTaskStatus.choices())
    message = models.TextField(blank=True)


class TaskLog(TimeStampedModel):
    task_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=PipelineTaskStatus.choices(), default=PipelineTaskStatus.PENDING)
    message = models.TextField(blank=True)


class TaskResult(TimeStampedModel):
    task_id = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=PipelineTaskStatus.choices(), default=PipelineTaskStatus.PENDING)
    data = models.JSONField(blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)
