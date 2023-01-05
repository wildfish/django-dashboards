import uuid

from django.contrib.auth.mixins import AccessMixin
from django.db.models import Avg, Count, F, Max, Q
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin

from wildcoeus.pipelines import PipelineTaskStatus, config
from wildcoeus.pipelines.forms import PipelineStartForm
from wildcoeus.pipelines.log import logger
from wildcoeus.pipelines.models import (
    PipelineExecution,
    PipelineLog,
    TaskLog,
    TaskResult,
)
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.registry import pipeline_registry as registry
from wildcoeus.pipelines.runners.celery.tasks import run_pipeline, run_task
from wildcoeus.pipelines.runners.eager import Runner as EagerRunner
from wildcoeus.pipelines.status import FAILED_STATUES
from wildcoeus.pipelines.storage import get_log_path


class IsStaffRequiredMixin(AccessMixin):
    """Verify that the current user is_staff."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PipelineListView(IsStaffRequiredMixin, TemplateView):
    template_name = "wildcoeus/pipelines/pipeline_list.html"

    def get_context_data(self, **kwargs):
        qs = (
            PipelineExecution.objects.values("pipeline_id")
            .annotate(
                total_success=Count(
                    "pipeline_id", filter=Q(status=PipelineTaskStatus.DONE.value)
                ),
                total_failed=Count(
                    "pipeline_id",
                    filter=Q(status__in=FAILED_STATUES),
                ),
                last_ran=Max("started"),
            )
            .order_by("pipeline_id")
        )
        runs = {x["pipeline_id"]: x["total_success"] for x in qs}
        failed = {x["pipeline_id"]: x["total_failed"] for x in qs}
        last_ran = {x["pipeline_id"]: x["last_ran"] for x in qs}

        # todo: Wrong as it needs to be grouped on run_id when doing the average
        t_qs = (
            TaskResult.objects.values("pipeline_id")
            .annotate(average_runtime=Avg(F("completed") - F("started")))
            .order_by("pipeline_id")
        )

        average_runtime = {x["pipeline_id"]: x["average_runtime"] for x in t_qs}

        return {
            **super().get_context_data(**kwargs),
            "runs": runs,
            "failed": failed,
            "last_ran": last_ran,
            "average_runtime": average_runtime,
            "pipelines": registry.get_all_registered_pipelines(),
        }


class PipelineExecutionListView(IsStaffRequiredMixin, ListView):
    template_name = "wildcoeus/pipelines/pipeline_execution_list.html"
    paginate_by = 30

    def get_queryset(self):
        return PipelineExecution.objects.with_task_count().filter(
            pipeline_id=self.kwargs["slug"]
        )

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "slug": self.kwargs["slug"],
        }


class PipelineStartView(IsStaffRequiredMixin, FormView):
    template_name = "wildcoeus/pipelines/pipeline_start.html"
    form_class = PipelineStartForm

    def get_context_data(self, **kwargs):
        pipeline_cls = pipeline_registry.get_pipeline_class(self.kwargs["slug"])
        tasks = list(pipeline_cls.tasks.items())
        return {
            **super().get_context_data(**kwargs),
            "pipeline": pipeline_cls,
            "tasks": tasks,
        }

    def get_form_kwargs(self):
        pipeline_cls = pipeline_registry.get_pipeline_class(self.kwargs["slug"])

        return {
            **super().get_form_kwargs(),
            "pipeline_cls": pipeline_cls,
        }

    def form_valid(self, form):
        # generate an id for the new run
        self.run_id = str(uuid.uuid4())

        # are we starting it straight away or passing it off to celery to start
        if isinstance(config.Config().WILDCOEUS_DEFAULT_PIPELINE_RUNNER, EagerRunner):
            logger.debug("running pipeline in eager")
            # trigger in eager
            pipeline_cls = pipeline_registry.get_pipeline_class(self.kwargs["slug"])
            runner = EagerRunner()
            reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER

            pipeline_cls().start(
                run_id=self.run_id,
                input_data=form.cleaned_data,
                runner=runner,
                reporter=reporter,
            )
        else:
            logger.debug("running pipeline in celery")
            # trigger in celery
            run_pipeline.delay(
                pipeline_id=self.kwargs["slug"],
                input_data=form.cleaned_data,
                run_id=self.run_id,
            )

        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("wildcoeus.pipelines:results", args=(self.run_id,))


class TaskResultView(IsStaffRequiredMixin, TemplateView):
    template_name = "wildcoeus/pipelines/results_list.html"


class TaskResultListView(IsStaffRequiredMixin, ListView):
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


class LogListView(IsStaffRequiredMixin, TemplateView):
    template_name = "wildcoeus/pipelines/_log_list.html"

    def all_tasks_completed(self):
        return (
            TaskResult.objects.not_completed()
            .for_run_id(run_id=self.kwargs["run_id"])
            .count()
            == 0
        )

    def _get_orm_logs(self, run_id):
        logs = [
            (log.created, log.log_message)
            for log in PipelineLog.objects.filter(run_id=run_id)
        ]
        logs.extend(
            [
                (log.created, log.log_message)
                for log in TaskLog.objects.filter(run_id=run_id)
            ]
        )
        logs.sort(key=lambda x: x[0])

        return "\n".join(
            [f"[{log[0].strftime('%d/%b/%Y %H:%M:%S')}]: {log[1]}" for log in logs]
        )

    def get_logs(self, run_id):
        fs = config.Config().WILDCOEUS_LOG_FILE_STORAGE
        path = get_log_path(run_id)

        if fs.exists(path):
            with fs.open(path, "r") as f:
                logs = f.read()
        else:
            logs = self._get_orm_logs(run_id=run_id)

        return logs

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        #  286 status stops htmx from polling
        response.status_code = 286 if self.all_tasks_completed() else 200
        return response

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "logs": self.get_logs(kwargs["run_id"]),
        }


class TaskResultReRunView(IsStaffRequiredMixin, SingleObjectMixin, RedirectView):
    model = TaskResult

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        task = self.object.get_task_instance()
        if task is None:
            raise Http404()

        # start the task again
        if isinstance(config.Config().WILDCOEUS_DEFAULT_PIPELINE_RUNNER, EagerRunner):
            run_task(
                task_id=self.object.task_id,
                run_id=self.object.run_id,
                pipeline_id=self.object.pipeline_id,
                input_data=self.object.input_data,
                serializable_pipeline_object=None,
                serializable_task_object=None,
            )
        else:
            run_task.delay(
                task_id=self.object.task_id,
                run_id=self.object.run_id,
                pipeline_id=self.object.pipeline_id,
                input_data=self.object.input_data,
                serializable_pipeline_object=None,
                serializable_task_object=None,
            )

        response = super().get(request, *args, **kwargs)
        return response

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("wildcoeus.pipelines:results", args=(self.object.run_id,))
