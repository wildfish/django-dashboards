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
        pipeline_id = "1"  # todo make unique for each run
        return [
            pipeline_id,
            {"message": "hello"},
            EagerRunner(),  # todo get from settings - either on pipeline or django settings
            LoggingReporter(),  # todo: get from settings - either on pipeline or django settings
        ]

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pipeline_cls = registry.get_pipeline_class(kwargs["slug"])
        if pipeline_cls is None:
            raise Http404(f"Pipeline {kwargs['slug']} not found in registry")

        # start the pipeline
        pipeline_cls().start(*self.get_pipeline_context())

        return HttpResponseRedirect(reverse("datorum_pipelines:list"))
