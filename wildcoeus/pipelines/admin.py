from django.contrib import admin

from . import models


@admin.register(models.TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ("pipeline_id", "pipeline_task", "run_id", "status", "started", "completed")


@admin.register(models.PipelineExecution)
class PipelineExecutionAdmin(admin.ModelAdmin):
    list_display = ("pipeline_id", "run_id", "status", "started")


admin.site.register(models.PipelineLog)
admin.site.register(models.TaskLog)
admin.site.register(models.ValueStore)
