import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin

from datorum_pipelines.models import TaskResult
from datorum_pipelines.pipelines.registry import pipeline_registry as registry
from datorum_pipelines.reporters.logging import LoggingReporter
from datorum_pipelines.reporters.orm import ORMReporter
from datorum_pipelines.runners.celery import Runner as CeleryRunner
from datorum_pipelines.runners.eager import Runner as EagerRunner


class PipelineListView(LoginRequiredMixin, TemplateView):
    template_name = "datorum_pipelines/pipeline_list.html"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "pipelines": registry.get_all_registered_pipelines(),
        }


class PipelineStartView(LoginRequiredMixin, RedirectView):
    def get_pipeline_context(self):
        self.run_id = uuid.uuid4()
        return {
            "run_id": str(self.run_id),
            "input_data": {"message": "hello"},  # todo: can this be made from a form?
            "runner": CeleryRunner(),  # todo should this get from a setting - either on pipeline or django settings
            "reporter": LoggingReporter(),  # todo: should this get from a setting - either on pipeline or django settings
        }

    def get(self, request, *args, **kwargs):
        pipeline_cls = registry.get_pipeline_class(kwargs["slug"])
        if pipeline_cls is None:
            raise Http404(f"Pipeline {kwargs['slug']} not found in registry")

        # start the pipeline
        pipeline_cls().start(**self.get_pipeline_context())
        messages.add_message(request, messages.INFO, "Pipeline started")

        response = super().get(request, *args, **kwargs)
        return response

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("datorum_pipelines:run", args=(self.run_id,))


class PipelineRunView(LoginRequiredMixin, TemplateView):
    template_name = "datorum_pipelines/results_list.html"

    def get_context_data(self, **kwargs):
        task_results = TaskResult.objects.filter(run_id=kwargs["run_id"])
        return {
            **super().get_context_data(**kwargs),
            "task_results": task_results,
        }


class TaskResultReRunView(LoginRequiredMixin, SingleObjectMixin, RedirectView):
    model = TaskResult

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        reporter = LoggingReporter()
        task = self.object.get_task_instance(reporter)
        # todo: needs to run by either celery or eager - how do we know
        # start the task again
        task.start(
            pipeline_id=self.object.pipeline_id,
            run_id=self.object.run_id,
            input_data=self.object.input_data,
            reporter=reporter,
        )
        messages.add_message(request, messages.INFO, "Task has been re-ran")

        response = super().get(request, *args, **kwargs)
        return response

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("datorum_pipelines:run", args=(self.object.run_id,))
