import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from datorum_pipelines.pipelines.registry import pipeline_registry as registry
from datorum_pipelines.reporters.logging import LoggingReporter
from datorum_pipelines.reporters.orm import ORMReporter
from datorum_pipelines.runners.eager import EagerRunner
from datorum_pipelines.models import TaskResult


class PipelineListView(LoginRequiredMixin, TemplateView):
    template_name = "datorum_pipelines/pipeline_list.html"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "pipelines": registry.get_all_registered_pipelines(),
        }


class PipelineStartView(LoginRequiredMixin, TemplateView):
    template_name = ""

    def get_pipeline_context(self):
        run_id = uuid.uuid4()
        return {
            "run_id": str(run_id),
            "input_data": {"message": "hello"},  # todo: can this be made from a form?
            "runner": EagerRunner(),  # todo get from a setting - either on pipeline or django settings
            "reporter": LoggingReporter(),  # todo: get from a setting - either on pipeline or django settings
        }

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pipeline_cls = registry.get_pipeline_class(kwargs["slug"])
        if pipeline_cls is None:
            raise Http404(f"Pipeline {kwargs['slug']} not found in registry")

        # start the pipeline
        context = self.get_pipeline_context()
        pipeline_cls().start(**context)

        return HttpResponseRedirect(reverse("datorum_pipelines:run", args=(context["run_id"],)))


class PipelineRunView(LoginRequiredMixin, TemplateView):
    template_name = "datorum_pipelines/results_list.html"

    def get_context_data(self, **kwargs):
        task_results = TaskResult.objects.filter(run_id=kwargs["run_id"])
        return {
            **super().get_context_data(**kwargs),
            "task_results": task_results,
        }
