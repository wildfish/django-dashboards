from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from datorum_pipelines.pipelines.registry import pipeline_registry as registry
from datorum_pipelines.reporters.logging import LoggingReporter
from datorum_pipelines.reporters.orm import ORMReporter
from datorum_pipelines.runners.eager import EagerRunner


class PipelineListView(LoginRequiredMixin, TemplateView):
    template_name = "datorum_pipelines/pipeline_list.html"

    def get_context_data(self):
        return {
            **super().get_context_data(),
            "pipelines": registry.get_all_registered_pipelines(),
        }


class PipelineStartView(LoginRequiredMixin, TemplateView):
    template_name = ""

    def get_pipeline_context(self):
        return [
            {},
            EagerRunner(),  # todo get from settings - either on pipeline or django settings
            LoggingReporter(),  # todo: get from settings - either on pipeline or django settings
        ]

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pipeline = registry.get_pipeline_class(kwargs["pipeline_id"])
        if pipeline is None:
            raise Http404(f"Pipeline {kwargs['pipeline_id']} not found in registry")

        # start the pipeline
        pipeline().start(*self.get_pipeline_context())

        return HttpResponseRedirect(reverse("datorum_pipelines:list"))
