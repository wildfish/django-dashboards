import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin

from wildcoeus.pipelines import config
from wildcoeus.pipelines.log import logger
from wildcoeus.pipelines.models import PipelineExecution, TaskResult
from wildcoeus.pipelines.registry import pipeline_registry as registry
from wildcoeus.pipelines.reporters.logging import LoggingReporter
from wildcoeus.pipelines.runners.celery.tasks import run_pipeline
from wildcoeus.pipelines.runners.eager import Runner as EagerRunner


class PipelineListView(LoginRequiredMixin, TemplateView):
    template_name = "wildcoeus/pipelines/pipeline_list.html"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "pipelines": registry.get_all_registered_pipelines(),
        }


class PipelineExecutionListView(LoginRequiredMixin, ListView):
    template_name = "wildcoeus/pipelines/pipeline_execution_list.html"

    def get_queryset(self):
        return PipelineExecution.objects.with_task_count().all()


class PipelineStartView(LoginRequiredMixin, RedirectView):
    def get_pipeline_context(self):
        return {
            "run_id": str(self.run_id),
            "input_data": {"message": "hello"},  # todo: can this be made from a form?
        }

    def get(self, request, *args, **kwargs):
        self.run_id = str(uuid.uuid4())

        # are we starting it straight away or passing it off to celery to start
        if isinstance(config.Config().WILDCOEUS_DEFAULT_PIPELINE_RUNNER, EagerRunner):
            logger.debug("running pipeline in eager")
            # trigger in eager
            run_pipeline(
                pipeline_id=kwargs["slug"],
                input_data={"message": "hello"},
                run_id=self.run_id,
            )
        else:
            logger.debug("running pipeline in celery")
            # trigger in celery
            run_pipeline.delay(
                pipeline_id=kwargs["slug"],
                input_data={"message": "hello"},
                run_id=self.run_id,
            )

        response = super().get(request, *args, **kwargs)
        return response

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("wildcoeus.pipelines:results", args=(self.run_id,))


class TaskResultView(LoginRequiredMixin, TemplateView):
    template_name = "wildcoeus/pipelines/results_list.html"


class TaskResultListView(LoginRequiredMixin, ListView):
    template_name = "wildcoeus/pipelines/_results_list.html"

    def get_queryset(self):
        return TaskResult.objects.for_run_id(run_id=self.kwargs["run_id"])

    def all_tasks_completed(self):
        return (
            TaskResult.objects.not_completed()
            .for_run_id(run_id=self.kwargs["run_id"])
            .count()
            == 0
        )

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        #  286 status stops htmx from polling
        response.status_code = 286 if self.all_tasks_completed() else 200
        return response


class TaskResultReRunView(LoginRequiredMixin, SingleObjectMixin, RedirectView):
    model = TaskResult

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        reporter = LoggingReporter()
        task = self.object.get_task_instance(reporter)
        if task is None:
            raise Http404()
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
        return reverse_lazy("wildcoeus.pipelines:run", args=(self.object.run_id,))
