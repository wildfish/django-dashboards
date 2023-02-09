from django import forms
from django.db.models import Q

from wildcoeus.pipelines.models import PipelineLog
from wildcoeus.pipelines.results.base import (
    BasePipelineResult,
    BaseTaskExecution,
    BaseTaskResult,
)
from wildcoeus.pipelines.results.helpers import (
    get_pipeline_result,
    get_task_execution,
    get_task_executions,
    get_task_result,
    get_task_results,
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

        if self.cleaned_data["type"] == BasePipelineResult.content_type_name:
            pipeline_results = [get_pipeline_result(self.cleaned_data["id"])]
            pipeline_result_id = pipeline_results[0].get_id()

            task_executions = get_task_executions(pipeline_result_id=pipeline_result_id)
            task_results = get_task_results(pipeline_result_id=pipeline_result_id)
        elif self.cleaned_data["type"] == BaseTaskExecution.content_type_name:
            pipeline_results = []
            task_executions = [get_task_execution(self.cleaned_data["id"])]
            task_results = get_task_results(
                task_execution_id=task_executions[0].get_id()
            )
        elif self.cleaned_data["type"] == BaseTaskResult.content_type_name:
            pipeline_results = []
            task_executions = []
            task_results = [get_task_result(self.cleaned_data["id"])]
        else:
            pipeline_results = []
            task_executions = []
            task_results = []

        return PipelineLog.objects.filter(
            Q(
                context_type=BasePipelineResult.content_type_name,
                context_id__in=[pr.get_id() for pr in pipeline_results],
            )
            | Q(
                context_type=BaseTaskExecution.content_type_name,
                context_id__in=[te.get_id() for te in task_executions],
            )
            | Q(
                context_type=BaseTaskResult.content_type_name,
                context_id__in=[tr.get_id() for tr in task_results],
            )
        )
