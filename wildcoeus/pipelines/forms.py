from django import forms
from django.db.models import Q

from wildcoeus.pipelines.models import (
    PipelineLog,
    PipelineResult,
    TaskExecution,
    TaskResult,
)


class PipelineStartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pipeline_cls = kwargs.pop("pipeline_cls")
        super().__init__(*args, **kwargs)

        # create form fields for each InputType on a task
        tasks = pipeline_cls.tasks.values() if pipeline_cls.tasks else []

        for task in tasks:
            if task.InputType:
                for f in task.InputType.__fields__.values():
                    self.fields[f"{f.name}"] = forms.CharField(required=f.required)


class LogFilterForm(forms.Form):
    type = forms.CharField()
    id = forms.CharField()

    @property
    def qs(self):
        if not self.is_valid():
            return PipelineLog.objects.all()

        if self.cleaned_data["type"] == "PipelineResult":
            pipeline_results = PipelineResult.objects.filter(id=self.cleaned_data["id"])
            task_executions = TaskExecution.objects.filter(
                pipeline_result_id=self.cleaned_data["id"]
            )
            task_results = TaskResult.objects.filter(
                execution__pipeline_result_id=self.cleaned_data["id"]
            )
        elif self.cleaned_data["type"] == "TaskExecution":
            pipeline_results = PipelineResult.objects.none()
            task_executions = TaskExecution.objects.filter(id=self.cleaned_data["id"])
            task_results = TaskResult.objects.filter(
                execution_id=self.cleaned_data["id"]
            )
        elif self.cleaned_data["type"] == "TaskResult":
            pipeline_results = PipelineResult.objects.none()
            task_executions = TaskExecution.objects.none()
            task_results = TaskResult.objects.filter(id=self.cleaned_data["id"])
        else:
            pipeline_results = PipelineResult.objects.none()
            task_executions = TaskExecution.objects.none()
            task_results = TaskResult.objects.none()

        return PipelineLog.objects.filter(
            Q(
                context_type="PipelineResult",
                context_id__in=list(pipeline_results.values_list("id", flat=True)),
            )
            | Q(
                context_type="TaskExecution",
                context_id__in=list(task_executions.values_list("id", flat=True)),
            )
            | Q(
                context_type="TaskResult",
                context_id__in=list(task_results.values_list("id", flat=True)),
            )
        )
