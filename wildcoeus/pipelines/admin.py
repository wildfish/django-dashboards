from django.contrib import admin

from . import models


@admin.register(models.TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = (
        "pipeline_id",
        "pipeline_task",
        "run_id",
        "serializable_pipeline_object",
        "serializable_task_object",
        "status",
        "started",
        "completed",
    )


@admin.register(models.PipelineExecution)
class PipelineExecutionAdmin(admin.ModelAdmin):
    list_display = (
        "pipeline_id",
        "run_id",
        "serializable_pipeline_object",
        "status",
        "started",
    )


@admin.register(models.TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ("log_message", "created")
    list_filter = ("run_id",)


@admin.register(models.PipelineLog)
class PipelineLogAdmin(admin.ModelAdmin):
    list_display = ("log_message", "created")
    list_filter = ("run_id",)


admin.site.register(models.ValueStore)
