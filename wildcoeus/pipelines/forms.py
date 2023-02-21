from django import forms
from django.db.models import Q

from wildcoeus.pipelines.models import PipelineLog
from wildcoeus.pipelines.results.base import PipelineResult, TaskExecution, TaskResult
from wildcoeus.pipelines.results.helpers import (
    get_pipeline_result,
    get_task_execution,
    get_task_executions,
    get_task_result,
    get_task_results,
)


class PipelineStartForm(forms.Form):
    """
    Form to clean the input for starting a form
    """

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
    """
    Form for filtering pipeline logs based on the type and id of the selected object
    """
    type = forms.CharField()
    """The type of object to filter logs by"""

    id = forms.CharField()
    """The id of the object to filter objects by"""

    @property
    def qs(self):
        """
        Queryset representing the filtered set of log objects
        """
        if not self.is_valid():
            return PipelineLog.objects.all()

        if self.cleaned_data["type"] == PipelineResult.content_type_name:
            pipeline_result = get_pipeline_result(self.cleaned_data["id"])
            pipeline_results = [pipeline_result] if pipeline_result else []
            pipeline_result_id = pipeline_result.get_id() if pipeline_result else None

            task_executions = get_task_executions(pipeline_result_id=pipeline_result_id)
            task_results = get_task_results(pipeline_result_id=pipeline_result_id)
        elif self.cleaned_data["type"] == TaskExecution.content_type_name:
            pipeline_results = []

            task_execution = get_task_execution(self.cleaned_data["id"])
            task_executions = [task_execution] if task_execution else []
            task_results = get_task_results(
                task_execution_id=task_execution.get_id() if task_execution else None
            )
        elif self.cleaned_data["type"] == TaskResult.content_type_name:
            pipeline_results = []
            task_executions = []
            task_result = get_task_result(self.cleaned_data["id"])
            task_results = [task_result] if task_result else []
        else:
            pipeline_results = []
            task_executions = []
            task_results = []

        return PipelineLog.objects.filter(
            Q(
                context_type=PipelineResult.content_type_name,
                context_id__in=[pr.get_id() for pr in pipeline_results],
            )
            | Q(
                context_type=TaskExecution.content_type_name,
                context_id__in=[te.get_id() for te in task_executions],
            )
            | Q(
                context_type=TaskResult.content_type_name,
                context_id__in=[tr.get_id() for tr in task_results],
            )
        )
